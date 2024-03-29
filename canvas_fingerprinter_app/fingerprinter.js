// Source: https://github.com/fingerprintjs/fingerprintjs/blob/master/src/sources/canvas.ts
// - Modified for simplification

// generateTextFP creates a text-based canvas fingerprint.
function GenerateTextFP(canvas, context) {

    // build the base
    canvas.width = 240
    canvas.height = 60
    context.textBaseline = 'alphabetic'
    context.fillStyle = '#f60'
    context.fillRect(100, 1, 62, 20)

    // define text to draw
    const printedText = `Cwm fjordbank gly ${String.fromCharCode(55357, 56835) /* 😃 */}`

    // first print
    context.fillStyle = '#069'
    context.font = '11pt "Times New Roman"'
    context.fillText(printedText, 2, 15)

    // second print
    context.fillStyle = 'rgba(102, 204, 0, 0.2)'
    context.font = '18pt Arial'
    context.fillText(printedText, 4, 45)

    // collect fp
    const fp = canvas.toDataURL()
    return fp
}
