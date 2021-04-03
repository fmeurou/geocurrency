/* Handle event that triggers a search for currencies */
(() => {
    const application = Stimulus.Application.start()

    let timer = null;

    application.register("currencies", class extends Stimulus.Controller {
        connect() {
            console.log("Hello, Currencies!", this.element)
        }

        search() {
            let value = this.element.value;
            clearTimeout(timer);
            timer = setTimeout(function () {
                let socket = new WebSocket('ws://127.0.0.1:8000/currencies');
                socket.onopen = function (e) {
                    socket.send(value);
                };
                socket.onmessage = function (event) {
                    $("#currencies_stream").html(event.data);
                };
            }, 500);
        }
    })
})()