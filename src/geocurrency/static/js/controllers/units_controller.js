/* Update destination units when changing source units */
(() => {
    const application = Stimulus.Application.start()

    application.register("units", class extends Stimulus.Controller {
        connect() {
            console.log("Hello, Units!", this.element)
        }

        compatible() {
            var value = this.element.value;
            var socket = new WebSocket('ws://127.0.0.1:8000/units');
            socket.onopen = function (e) {
                socket.send(value);
            };
            socket.onmessage = function (event) {
                $("#dest_units_list").html(event.data);
            };
        }
    })
})()