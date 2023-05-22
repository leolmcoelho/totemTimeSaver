const Keyboard = {
    elements: {
        main: null,
        keysContainer: null,
        keys: []
    },

    eventHandlers: {
        oninput: null,
        onclose: null
    },

    properties: {
        value: "",
        capslock: false
    },

    init() {
        // Create main elements
        this.elements.main = document.createElement("div");
        this.elements.keysContainer = document.createElement("div");

        // Setup main elements
        this.elements.main.classList.add("keyboard", "keyboard--hidden");
        this.elements.keysContainer.classList.add("keyboard__keys");
        this.elements.keysContainer.appendChild(this._createKeys());

        this.elements.keys = this.elements.keysContainer.querySelectorAll(".keyboard__key");

        // Add to DOM
        this.elements.main.appendChild(this.elements.keysContainer);
        document.body.appendChild(this.elements.main);

        // Automatically use keyboard for elements
        document.querySelectorAll(".use-keyboard-input").forEach(element => {
            element.addEventListener("focus", () => {
                this.open(element.value, currentValue => {
                    element.value = currentValue;
                });
            });
        });

        let space = document.querySelector("body > div > div > button.keyboard__key.keyboard__key--extra--wide");

        space.style = 'max-width: 25%; width: 40%;'
    
    },

    _createKeys() {
        const fragment = document.createDocumentFragment();
        const keyLayout = [
           
            "Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P","backspace",
            "caps", "A", "S", "D", "F", "G", "H", "J", "K", "L", "done",
             "Z", "X", "C", "V", "B", "N", "M",
            "space"
        ];

        // Creates HTML for an icon
        const createIconHTML = (icon_name) => {
            return `<i class="material-icons">${icon_name}</i>`;
        };

        keyLayout.forEach(key => {
            const keyELement = document.createElement("button");
            const insertLineBreak = ["done", "backspace",  "M"].indexOf(key) !== -1;

            // Add attributes/classes
            keyELement.setAttribute("type", "button");
            keyELement.classList.add("keyboard__key");

            switch (key) {
                case "backspace":
                    keyELement.classList.add("keyboard__key--wide");
                    keyELement.innerHTML = createIconHTML("backspace");

                    keyELement.addEventListener("click", () => {
                        this.properties.value = this.properties.value.substring(0, this.properties.value.length - 1);
                        this._triggerEvent("oninput");
                    });

                    break;

                case "caps":
                    keyELement.classList.add("keyboard__key--wide", "keyboard__key--activatable");
                    keyELement.innerHTML = createIconHTML("keyboard_capslock");

                    keyELement.addEventListener("click", () => {
                        this._toogleCapsLock();
                        keyELement.classList.toggle("keyboard__key--active", this.properties.capslock);
                    });

                    break;

                case "enter":
                    keyELement.classList.add("keyboard__key--wide");
                    keyELement.innerHTML = createIconHTML("keyboard_return");

                    keyELement.addEventListener("click", () => {
                        this.properties.value += "\n";
                        this._triggerEvent("oninput");
                    });

                    break;

                case "space":
                    keyELement.classList.add("keyboard__key--extra--wide");
                    keyELement.innerHTML = createIconHTML("space_bar");

                    keyELement.addEventListener("click", () => {
                        this.properties.value += " ";
                        this._triggerEvent("oninput");
                    });

                    break;

                case "done":
                    keyELement.classList.add("keyboard__key--wide", "keyboard__key--dark");
                    keyELement.innerHTML = createIconHTML("check_circle");

                    keyELement.addEventListener("click", () => {
                        this.close();
                        this._triggerEvent("onclose");
                    });

                    break;

                default:
//                    key = key.toUpperCase();
                    keyELement.textContent = key.toUpperCase();

                    keyELement.addEventListener("click", () => {
                        this.properties.value += this.properties.capslock ? key.toLowerCase() : key.toUpperCase();
                        this._triggerEvent("oninput");
                    });

                    break;

            }

            fragment.appendChild(keyELement);

            if (insertLineBreak) {
                fragment.appendChild(document.createElement("br"));
            }

        });

        return fragment;
    },

    _triggerEvent(handlerName) {
        if (typeof this.eventHandlers[handlerName] == "function") {
            this.eventHandlers[handlerName](this.properties.value);
        }
    },

    _toogleCapsLock() {
        this.properties.capslock = !this.properties.capslock;

        for (const key of this.elements.keys) {
            if (key.childElementCount === 0) {
                key.textContent = this.properties.capslock ? key.textContent.toUpperCase() : key.textContent.toLowerCase();
            }
        }
    },

    open(initialValue, oninput, onclose) {
        this.properties.value = initialValue || "";
        this.eventHandlers.oninput = oninput;
        this.eventHandlers.onclose = onclose;
        this.elements.main.classList.remove("keyboard--hidden");
    },

    close() {
        this.properties.value = "";
        this.eventHandlers.oninput = oninput;
        this.eventHandlers.onclose = onclose;
        this.elements.main.classList.add("keyboard--hidden");
    }
};

window.addEventListener("DOMContentLoaded", function () {
    Keyboard.init();

});