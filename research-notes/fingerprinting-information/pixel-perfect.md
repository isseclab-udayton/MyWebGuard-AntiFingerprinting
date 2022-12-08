# Pixel Perfect: Fingerprinting Canvas in HTML5

<https://hovav.net/ucsd/dist/canvas.pdf>

## Summary

The researchers propose fingerprinting using a `<canvas>` element. A site can embed a canvas element and check its pixel rendering to fingerprint the client. This is possible because of the closer relationship between modern browsers and computer hardware, which means the differences in rendering can uniquely identify the client.

- (Note that, although Torbutton disables WebGL, it allows text rendering to a , and is thus at present partly vulnerable to our fingerprint.)
- Canvas: Could we possibly monitor:
  - `getImageData()`
  - `toDataURL(type)` – passed and image/png
    - if this is hashed and sent somewhere
  - how the canvas image is drawn – a specially crafted one is used to create fingerprints that are as unique as possible- they used “How quickly daft jumping zebras vex.” With more punctuation symbols
- WebFonts: they attach their fingerprinter to a successful font load
- Uses a pangram to generate canvas images
- Requests and invalid font to see what the system defaults to
- Given these results, we conclude that rendering a simple pangram in Arial on a `<canvas>` is enough to leak the user’s operating system family and (almost always) browser family.
