function generate() {
    fetch("http://127.0.0.1:5000/api/mimicry-sentence")
        .then(function (data) {
            return data.json();
        })
        .then(function (json) {
            const data = json.context
            const elem = document.getElementById('output')
            elem.textContent = data
        })
}
