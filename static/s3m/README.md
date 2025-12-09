# S3M Tracker Music Demo

This directory contains a demo of S3M tracker music files using the js-dos emulator.

## Third-Party Library

**js-dos.js** - DOSBox JavaScript emulator
- **Purpose**: Runs DOS-based tracker music player in browser
- **Source**: https://js-dos.com/ (or js-dos v6)
- **License**: GPL-2.0 (verify with original source)
- **Version**: Minified, version unknown (should be pinned/documented)
- **Security Note**: This minified library uses `innerHTML` for DOM manipulation. This is acceptable as a trusted third-party emulator library, but should be noted for security audits.

## Files

- `js-dos.js` - DOSBox emulator library (minified)
- `js-dos.css` - Emulator styling
- `it.jsdos` - DOSBox configuration bundle
- `it.html` - Demo page
- `*.s3m` - S3M tracker music files
- `*.mp3` - MP3 versions of the music

## Usage

The demo is accessible at `/s3m/it.html` and loads tracker music files in the browser using the DOSBox emulator.

## Security Considerations

- js-dos.js is a minified third-party library
- Uses `innerHTML` internally (unavoidable for emulator functionality)
- Only loads from trusted static files in this directory
- Page is marked as static in test configuration (static files not processed by regular validation)

## Maintenance

- Consider pinning specific js-dos version
- Verify library integrity with SRI hash
- Check for security updates periodically
