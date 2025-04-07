import azure.functions as func
import logging

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

@app.route(route="http_trigger")
def http_trigger(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    base_message = "Hello from Azure Function..."
    if name:
        base_message = f"Hello, {name} from Azure Function..."

    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Azure Function Demoscene</title>
        <style>
            body {{ background: #000; margin: 0; overflow: hidden; }}
            canvas {{ display: block; }}
        </style>
    </head>
    <body>
        <canvas id="canvas"></canvas>
        <script>
            const canvas = document.getElementById('canvas');
            const ctx = canvas.getContext('2d');
            let w, h;

            function resize() {{
                w = canvas.width = window.innerWidth;
                h = canvas.height = window.innerHeight;
            }}
            window.addEventListener('resize', resize);
            resize();

            // Max radius exceeds screen diagonal
            const maxRadius = Math.sqrt(w * w + h * h) * 1.5;

            // 4 bitplanes with moving oversized circles
            const bitplanes = [
                {{ x: w * 0.3, y: h * 0.3, dx: 1, dy: 1, color: '#ff0000', bit: 1 }}, // Red
                {{ x: w * 0.7, y: h * 0.3, dx: -1, dy: 1, color: '#00ff00', bit: 2 }}, // Green
                {{ x: w * 0.5, y: h * 0.7, dx: 1, dy: -1, color: '#0000ff', bit: 4 }}, // Blue
                {{ x: w * 0.4, y: h * 0.5, dx: -1, dy: -1, color: '#ffff00', bit: 8 }} // Yellow
            ];

            // Scroll text setup
            const message = "{base_message}    ";
            const textHeight = 40;
            const textY = h / 2 - textHeight / 2;
            let textX = w;

            function draw() {{
                ctx.fillStyle = '#000'; // Clear screen
                ctx.fillRect(0, 0, w, h);

                // Draw each bitplane directly with additive blending
                ctx.globalCompositeOperation = 'screen'; // Additive blending for bitplane simulation
                bitplanes.forEach(bp => {{
                    bp.x += bp.dx;
                    bp.y += bp.dy;
                    if (bp.x < 0 || bp.x > w) bp.dx *= -1;
                    if (bp.y < 0 || bp.y > h) bp.dy *= -1;

                    for (let r = maxRadius; r > 0; r -= 50) {{
                        ctx.beginPath();
                        ctx.arc(bp.x, bp.y, r, 0, Math.PI * 2);
                        ctx.lineWidth = 20;
                        ctx.strokeStyle = bp.color;
                        ctx.stroke();
                    }}
                }});
                ctx.globalCompositeOperation = 'source-over'; // Reset to default

                // Draw text rectangle overlay
                ctx.fillStyle = '#000';
                ctx.fillRect(0, textY, w, textHeight);

                // Draw scrolling text
                ctx.font = `${{textHeight - 10}}px monospace`;
                ctx.fillStyle = '#0f0';
                ctx.textAlign = 'left';
                ctx.textBaseline = 'middle';
                ctx.fillText(message, textX, textY + textHeight / 2);

                // Scroll text
                textX -= 2;
                const textWidth = ctx.measureText(message).width;
                if (textX < -textWidth) textX = w;

                requestAnimationFrame(draw);
            }}
            draw();
        </script>
    </body>
    </html>
    """

    return func.HttpResponse(
        html_content,
        mimetype="text/html",
        status_code=200
    )
