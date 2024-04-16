
const canvas = document.createElement('canvas')
canvas.classList.add("page-background")
const elem = document.querySelector("body")
elem.prepend(canvas)

function paintBackground() {

    canvas.width = window.innerWidth
    canvas.height = window.innerHeight
    const ctx = canvas.getContext('2d')

    const strokeGap = Math.floor(canvas.width / 20)

    for (let x = 0; x < canvas.width; x += strokeGap) {
        ctx.beginPath()
        ctx.moveTo(x, 0)
        ctx.lineTo(x, canvas.height)
        ctx.strokeStyle = "rgba(255,255,255,1)"
        ctx.stroke()
    }
}

paintBackground()
addEventListener("resize", (event) => { paintBackground() });