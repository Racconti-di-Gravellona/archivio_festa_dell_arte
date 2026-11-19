import AppKit
import Foundation

let W: CGFloat = 1200
let H: CGFloat = 630

func color(_ hex: UInt32, _ a: CGFloat = 1) -> NSColor {
    NSColor(srgbRed: CGFloat((hex >> 16) & 0xFF)/255.0,
            green: CGFloat((hex >> 8) & 0xFF)/255.0,
            blue: CGFloat(hex & 0xFF)/255.0,
            alpha: a)
}

func font(_ names: [String], _ size: CGFloat) -> NSFont {
    for n in names { if let f = NSFont(name: n, size: size) { return f } }
    return NSFont.systemFont(ofSize: size, weight: .bold)
}

let rep = NSBitmapImageRep(bitmapDataPlanes: nil, pixelsWide: Int(W), pixelsHigh: Int(H),
                           bitsPerSample: 8, samplesPerPixel: 4, hasAlpha: true, isPlanar: false,
                           colorSpaceName: .deviceRGB, bytesPerRow: 0, bitsPerPixel: 0)!
NSGraphicsContext.saveGraphicsState()
NSGraphicsContext.current = NSGraphicsContext(bitmapImageRep: rep)
let ctx = NSGraphicsContext.current!.cgContext
ctx.setAllowsAntialiasing(true)
ctx.setShouldAntialias(true)

// sfondo
let bg = NSGradient(colors: [color(0xFCFAF7), color(0xF5EDE4)])!
bg.draw(in: NSRect(x: 0, y: 0, width: W, height: H), angle: -20)

// alone terracotta dietro il logo
let halo = NSBezierPath(ovalIn: NSRect(x: 40, y: 115, width: 400, height: 400))
color(0xF1DFD3, 0.9).setFill(); halo.fill()

// logo arrotondato con ombra
let logoPath = "assets/favicon/android-chrome-512x512.png"
if let logo = NSImage(contentsOfFile: logoPath) {
    let s: CGFloat = 300
    let r = NSRect(x: 90, y: (H - s)/2, width: s, height: s)
    let shadow = NSShadow()
    shadow.shadowColor = color(0x5A3A2A, 0.28)
    shadow.shadowBlurRadius = 26
    shadow.shadowOffset = NSSize(width: 0, height: -10)
    NSGraphicsContext.saveGraphicsState()
    shadow.set()
    let clip = NSBezierPath(roundedRect: r, xRadius: 46, yRadius: 46)
    color(0xFFFFFF).setFill(); clip.fill()
    NSGraphicsContext.restoreGraphicsState()

    NSGraphicsContext.saveGraphicsState()
    NSBezierPath(roundedRect: r, xRadius: 46, yRadius: 46).addClip()
    logo.draw(in: r, from: .zero, operation: .sourceOver, fraction: 1)
    NSGraphicsContext.restoreGraphicsState()
}

let left: CGFloat = 470

func draw(_ text: String, font f: NSFont, color c: NSColor, x: CGFloat, y: CGFloat, tracking: CGFloat = 0) {
    let attrs: [NSAttributedString.Key: Any] = [.font: f, .foregroundColor: c, .kern: tracking]
    (text as NSString).draw(at: NSPoint(x: x, y: y), withAttributes: attrs)
}

// occhiello
draw("ARCHIVIO", font: font(["HelveticaNeue-Bold", "Arial-BoldMT"], 28), color: color(0xB2441D), x: left, y: 470, tracking: 6)

// titolo
let titleFont = font(["PlayfairDisplay-Bold", "Didot-Bold", "Baskerville-Bold", "Georgia-Bold"], 96)
draw("Festa", font: titleFont, color: color(0x1C1917), x: left, y: 330)
draw("dell’Arte", font: titleFont, color: color(0x1C1917), x: left, y: 220)

// linea
color(0xC85A32).setFill()
NSBezierPath(roundedRect: NSRect(x: left, y: 185, width: 120, height: 6), xRadius: 3, yRadius: 3).fill()

// sottotitolo
draw("Gravellona Lomellina  ·  1995–2026", font: font(["HelveticaNeue-Medium", "ArialMT"], 30), color: color(0x57534E), x: left, y: 130, tracking: 0.5)

NSGraphicsContext.restoreGraphicsState()

let png = rep.representation(using: .png, properties: [:])!
try! png.write(to: URL(fileURLWithPath: "assets/social/anteprima-social-1200x630.png"))
print("ok")
