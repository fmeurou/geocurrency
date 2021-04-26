"""
Serializers for Calculations module
"""
import json

import pint
from rest_framework import serializers
from sympy import sympify, SympifyError

from geocurrency.units.models import UnitSystem
from .models import Expression, CalculationPayload, Operand, \
    CalculationResult, CalculationResultError, CalculationResultDetail


class OperandSerializer(serializers.Serializer):
    """
    Serialize an Operand
    """
    name = serializers.CharField(
        label="Name of the operand in the expression",
        help_text="{a} in an expression should have an operand named 'a'")
    value = serializers.FloatField(
        label="Value of the operand as a float")
    unit = serializers.CharField(
        label="Units of the operand as a string")
    uncertainty = serializers.CharField(
        label="Uncertainty value, either absolute, or percentage.",
        required=False,
        help_text="Uncertainty for value, "
                  "if float, it is absolute (10), "
                  "else, it must contain % (12%)")

    def is_valid(self, raise_exception=False) -> bool:
        """
        Check validity of the operand
        """
        if not self.initial_data.get('name'):
            raise serializers.ValidationError("operand Name not set")
        if 'value' not in self.initial_data:
            raise serializers.ValidationError("operand Value not set")
        try:
            float(self.initial_data['value'])
        except ValueError as e:
            raise serializers.ValidationError("invalid operand value") from e
        if 'unit' not in self.initial_data:
            raise serializers.ValidationError("operand Unit not set")
        return super().is_valid(raise_exception=raise_exception)

    def create(self, validated_data):
        """
        Create an Operand object
        :param validated_data: cleaned date
        """
        return Operand(**validated_data)


class ExpressionListSerializer(serializers.ListSerializer):
    """
    Serialize a list of Expressions
    """

    def is_valid(self,
                 unit_system: UnitSystem,
                 dimensions_only=False,
                 raise_exception=False):
        """
        Check validity of expression with a specific UnitSystem
        :param unit_system: UnitSystem instance
        :param dimensions_only: Only check dimensionality, not actual units
        :param raise_exception: raise an exception instead of a list of errors
        """
        super().is_valid(raise_exception=raise_exception)
        for initial_exp in self.initial_data:
            ec = ExpressionSerializer(data=initial_exp)
            ec.is_valid(unit_system=unit_system,
                        dimensions_only=dimensions_only)
            if ec.errors:
                self._errors.append(ec.errors)
        return not bool(self._errors)


class ExpressionSerializer(serializers.Serializer):
    """
    Serialize an expression
    """
    unit_system = None
    key = None
    expression = serializers.CharField(
        label="Mathematical expression to evaluate",
        required=True,
        help_text="Operands must be placed between curly braces."
                  "A recommended expression format "
                  "would be '{a}+{b}*{c}'")
    operands = OperandSerializer(
        label="List of operands",
        many=True,
        required=True)
    out_units = serializers.CharField(
        label="Define output units",
        required=False,
        help_text="Set output units, optional (e.g.: km/hour)")

    class Meta:
        """
        Meta
        """
        list_serializer_class = ExpressionListSerializer

    def is_valid(self, unit_system: UnitSystem,
                 raise_exception=False,
                 dimensions_only=False) -> bool:
        """
        Check if expression is valid
        :param unit_system: UnitSystem instance
        :param dimensions_only: Only test dimensions
        :param raise_exception: raise an exception instead of a list of errors
        """
        super().is_valid(raise_exception=raise_exception)
        operands = self.operands_validation(
            operands=self.initial_data.get('operands')
        )
        expression = self.expression_validation(
            expression=self.initial_data.get('expression'),
            operands=operands
        )
        out_units = self.out_units_validation(
            unit_system=unit_system,
            out_units=self.initial_data.get('out_units')
        )
        if expression:
            if dimensions_only:
                self.dimensions_validation(
                    unit_system=unit_system,
                    expression=expression,
                    operands=operands,
                    out_units=out_units
                )
            else:
                self.units_validation(
                    unit_system=unit_system,
                    expression=expression,
                    operands=operands,
                    out_units=out_units
                )
        if self._errors and raise_exception:
            raise serializers.ValidationError(self._errors)
        return not bool(self._errors)

    def units_validation(self,
                         unit_system: UnitSystem,
                         expression: str,
                         operands: [Operand],
                         out_units: str = None) -> bool:
        """
        Validate units based on the units of the operands
        :param unit_system: Reference unit system with custom units
        :param expression: Mathematical expression as string
        :param operands: list of Operand objects
        :param out_units: optional conversion to specific units
        """
        # Validate units
        q_ = unit_system.ureg.Quantity
        try:
            units_kwargs = {
                v['name']: q_(v['value'], v['unit'])
                for v in operands}
            result = unit_system.ureg.parse_expression(
                expression, **units_kwargs)
        except KeyError:
            self._errors['operands'] = "Missing operands"
            return False
        except pint.errors.DimensionalityError:
            self._errors['expression'] = "Incoherent dimension"
            return False
        if out_units:
            try:
                result.to(out_units)
            except pint.errors.DimensionalityError:
                self._errors['out_units'] = "Incoherent output dimension"
                return False
        return True

    def dimensions_validation(self,
                              unit_system: UnitSystem,
                              expression: str,
                              operands: [Operand],
                              out_units: str = None) -> bool:
        """
        Validate units dimensions based on get_unit of the operands
        :param unit_system: Reference unit system with custom units
        :param expression: Mathematical expression as string
        :param operands: list of Operand objects
        :param out_units: optional conversion to specific units
        """
        q_ = unit_system.ureg.Quantity
        operand_objs = [
            Operand(
                name=v['name'],
                value=v['value'],
                unit=v['unit'])
            for v in operands]
        units_kwargs = {v.name: f"{v.value} {v.get_unit(unit_system)}"
                        for v in operand_objs}
        try:
            result = q_(expression.format(**units_kwargs))
        except KeyError:
            self._errors['operands'] = "Missing operands"
            return False
        except pint.errors.DimensionalityError:
            self._errors['expression'] = "Incoherent dimension"
            return False
        if out_units:
            try:
                result.to(out_units)
            except pint.errors.DimensionalityError:
                self._errors['out_units'] = "Incoherent output dimension"
                return False
        return True

    def expression_validation(self, expression: str, operands: [Operand]):
        """
        Check syntactic validity of expression
        :param expression: Mathematical expression as string
        :param operands: list of Operand objects
        """
        if not expression:
            self._errors['expression'] = "Empty expression"
            return None
        # Validate syntax
        value_kwargs = {v['name']: v['value'] for v in operands}
        try:
            sympify(expression.format(**value_kwargs))
        except (SympifyError, KeyError):
            self._errors['expression'] = "Invalid operation"
        return expression

    def out_units_validation(self, unit_system: UnitSystem, out_units: str):
        """
        Check validity of output units
        :param unit_system: Reference unit system with custom units
        :param out_units: optional conversion to specific units
        """
        if not out_units:
            return None
        q_ = unit_system.ureg.Quantity
        try:
            q_(1, out_units)
        except pint.errors.DimensionalityError:
            self._errors['out_units'] = "Incoherent output dimension"
            return None
        return out_units

    def operands_validation(self, operands):
        """
        Validate Operand
        :param operands: Operand
        """
        errors = []
        try:
            for var in operands:
                vs = OperandSerializer(data=var)
                vs.is_valid()
                if vs.errors:
                    errors.append(vs.errors)
            if errors:
                self._errors['operands'] = errors
        except json.JSONDecodeError as e:
            self._errors['operands'] = f"Invalid operands json format: {e}"
        except TypeError:
            self._errors['operands'] = f"Invalid operands input"
        return operands

    def create(self, validated_data):
        """
        Create an Expression
        :param validated_data: cleaned data
        """
        operands = []
        for var in validated_data.get('operands'):
            vs = OperandSerializer(data=var)
            if vs.is_valid():
                operands.append(vs.create(vs.validated_data))
        return Expression(
            expression=validated_data.get('expression'),
            operands=operands,
            out_units=validated_data.get('out_units')
        )

    def update(self, instance, validated_data):
        """
        Update Expression
        :param instance: Expression object
        :param validated_data: cleaned data
        """
        instance.expression = validated_data.get('expression')
        instance.operands = validated_data.get('operands')
        instance.out_units = validated_data.get('out_units')
        return instance


class CalculationResultDetailSerializer(serializers.Serializer):
    """
    Serializer for the CalculationResultDetail class
    """
    expression = serializers.CharField(label="Expression to evaluate")
    operands = OperandSerializer(many=True)
    magnitude = serializers.FloatField(label="Magnitude of result")
    uncertainty = serializers.FloatField(label="Uncertainty of result")
    unit = serializers.CharField(label="Units of result")

    def create(self, validated_data):
        """
        Create a CalculationResultDetail object
        :param validated_data: cleaned data
        """
        return CalculationResultDetail(**validated_data)

    def update(self, instance, validated_data):
        """
        Update a CalculationResultDetail object
        :param instance: CalculationResultDetail object
        :param validated_data: cleaned data
        """
        instance.expression = validated_data.get(
            'expression', instance.expression)
        instance.operands = validated_data.get(
            'operands', instance.operands)
        instance.magnitude = validated_data.get(
            'magnitude', instance.magnitude)
        instance.uncertainty = validated_data.get(
            'uncertainty', instance.operands)
        return instance


class CalculationResultErrorSerializer(serializers.Serializer):
    """
    Serializer for the CalculationResultError class
    """
    expression = serializers.CharField(label="Expression to evaluate")
    operands = OperandSerializer(many=True)
    calc_date = serializers.DateField(label="Date of calculation")
    error = serializers.CharField(label="Error during calculation")

    def create(self, validated_data):
        """
        Create a CalculationResultError object
        :param validated_data: cleaned data
        """
        return CalculationResultError(**validated_data)

    def update(self, instance, validated_data):
        """
        Update a CalculationResultError object
        :param instance: CalculationResultError object
        :param validated_data: cleaned data
        """
        instance.expression = validated_data.get(
            'expression', instance.expression)
        instance.operands = validated_data.get(
            'operands', instance.operands)
        instance.calc_date = validated_data.get(
            'calc_date', instance.calc_date)
        instance.error = validated_data.get(
            'error', instance.error)
        return instance


class CalculationResultSerializer(serializers.Serializer):
    id = serializers.UUIDField(label="ID of the batch")
    detail = CalculationResultDetailSerializer(
        label="Details of the calculation", many=True)
    status = serializers.CharField(
        label="Status of the calculation")
    errors = CalculationResultErrorSerializer(
        label="Errors during calculation", many=True)

    def create(self, validated_data):
        """
        Create a CalculationResult object
        :param validated_data: cleaned data
        """
        return CalculationResult(**validated_data)

    def update(self, instance, validated_data):
        """
        Update a CalculationResult object
        :param instance: CalculationResult object
        :param validated_data: cleaned data
        """
        instance.id = validated_data.get('id', instance.id)
        instance.detail = validated_data.get('detail', instance.detail)
        instance.status = validated_data.get('status', instance.status)
        instance.errors = validated_data.get('errors', instance.errors)
        return instance


class CalculationPayloadSerializer(serializers.Serializer):
    """
    Serializer for CalculationPayload
    """
    unit_system = serializers.CharField(
        label="Unit system to evaluate in",
        required=True)
    data = ExpressionSerializer(
        label="Payload of expressions",
        many=True, required=False)
    batch_id = serializers.CharField(
        label="User defined ID of the batch of evaluations",
        required=False)
    key = serializers.CharField(
        label="User defined categorization key",
        required=False)
    eob = serializers.BooleanField(
        label="End of batch ? triggers the evaluation",
        default=False)

    def is_valid(self, raise_exception=False) -> bool:
        """
        Check validity of the payload
        """
        if not self.initial_data.get('data') and \
                (not self.initial_data.get('batch_id')
                 or (self.initial_data.get('batch_id')
                     and not self.initial_data.get('eob'))):
            raise serializers.ValidationError(
                'data has to be provided if batch_id is not provided '
                'or batch_id is provided and eob is False'
            )
        return super().is_valid(raise_exception=raise_exception)

    @staticmethod
    def validate_unit_system(value: str):
        """
        Validate unit system
        :param value: unit system name
        """
        from geocurrency.units.models import UnitSystem
        if not UnitSystem.is_valid(value):
            raise serializers.ValidationError('Invalid unit system')
        return value

    def create(self, validated_data: {}):
        """
        Create CalculationPayload from cleaned data
        :param validated_data: cleaned data
        """
        return CalculationPayload(**validated_data)

    def update(self, instance, validated_data: {}):
        """
        Update a CalculationPayload from cleaned data
        :param instance: CalculationPayload object
        :param validated_data: cleaned data
        """
        self.data = validated_data.get('data', instance.data)
        self.unit_system = validated_data.get(
            'unit_system', instance.unit_system)
        self.batch_id = validated_data.get('batch_id', instance.batch_id)
        self.key = validated_data.get('key', instance.key)
        self.eob = validated_data.get('eob', instance.eob)
        return instance
