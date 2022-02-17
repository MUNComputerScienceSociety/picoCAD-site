class PicoCADViewerElement extends HTMLElement {
  /*
  static get observedAttributes() {
    return ["c", "l"];
  }

  attributeChangedCallback(name, oldValue, newValue) {
    console.log("Custom square element attributes changed.");
  }
  */

  constructor() {
    super();
  }

  connectedCallback() {
    const div = document.createElement("div");

    const p = document.createElement("p");
    p.innerText = "Hello World";
    div.appendChild(p);

    this.appendChild(div);
  }
}

customElements.define("picocad-viewer", PicoCADViewerElement);
