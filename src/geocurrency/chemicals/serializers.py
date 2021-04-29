"""
Serializers for chemicals classes
"""
from functools import partial
from rest_framework import serializers


class ChemicalMetadataListSerializer(serializers.Serializer):
    """
    Serializer for ChemicalMetadata list
    """
    CHEMICAL_METADATA_FIELDS = [
        'CAS',
        'CASs',
        'InChI',
        'MW',
        'common_name',
        'formula',
        'pubchemid',
    ]
    CAS = serializers.SerializerMethodField(
        label="CAS number",
        read_only=True)
    CASs = serializers.SerializerMethodField(
        label="CAS String",
        read_only=True)
    InChI = serializers.SerializerMethodField(
        label="InChI",
        read_only=True)
    MW = serializers.SerializerMethodField(
        label="MW",
        read_only=True)
    common_name = serializers.SerializerMethodField(
        label="Common name",
        read_only=True)
    formula = serializers.SerializerMethodField(
        label="formula",
        read_only=True)
    pubchemid = serializers.SerializerMethodField(
        label="pubchemid",
        read_only=True)

    def create(self, validated_data):
        """
        Read only serializer
        """
        pass

    def update(self, instance, validated_data):
        """
        Read only serializer
        """
        pass

    def __getattribute__(self, name):
        if name.startswith('get') and \
                name.replace('get_', '') in self.CHEMICAL_METADATA_FIELDS:
            return partial(
                self.get_metadata_attr,
                attr=name.replace('get_', '')
            )
        return super().__getattribute__(name)

    def get_metadata_attr(self, obj, attr):
        if attr in self.CHEMICAL_METADATA_FIELDS:
            return getattr(obj, attr)
        return None


class ChemicalMetadataDetailSerializer(ChemicalMetadataListSerializer):
    """
    Serializer for ChemicalMetadata detail
    """
    CHEMICAL_METADATA_FIELDS = [
        'CAS',
        'CASs',
        'InChI',
        'InChI_key',
        'MW',
        'charge',
        'common_name',
        'formula',
        'iupac_name',
        'pubchemid',
        'smiles',
        'synonyms'
    ]
    CASs = serializers.SerializerMethodField(
        label="CAS string identifier",
        read_only=True)
    InChI_key = serializers.SerializerMethodField(
        label="InChI",
        read_only=True)
    iupac_name = serializers.SerializerMethodField(
        label="iupac name",
        read_only=True)
    synonyms = serializers.ListField(
        label="synonyms",
        read_only=True)
    smiles = serializers.SerializerMethodField(
        label="smiles",
        read_only=True)



