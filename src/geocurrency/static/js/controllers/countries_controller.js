/* Handle event that triggers a search for countries */
(() => {
    const application = Stimulus.Application.start()

    let timer = null;

    application.register("countries", class extends Stimulus.Controller {
        connect() {
            console.log("Hello, Stimulus!", this.element)
        }

        search() {
            clearTimeout(timer);
            let value = this.element.value;
            timer = setTimeout(function () {
                let socket = new WebSocket('ws://127.0.0.1:8000/countries');
                socket.onopen = function (e) {
                    socket.send(value);
                };
                socket.onmessage = function (event) {
                    $("#countries_stream").html(event.data);
                }
            }, 500);
        }
    })
})()