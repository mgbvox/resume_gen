"""Live-reload development server for resume preview.

This module provides an HTTP server with live reload capabilities for
previewing resumes during development. It watches for changes to
Markdown and CSS files and automatically refreshes the browser.

Example:
    Start the preview server::

        from pathlib import Path
        from resume_gen.server import run_server

        run_server(
            md_path=Path("resume.md"),
            css_path=Path("assets/modern.css"),
            port=8000,
            open_browser=True
        )

The server uses a polling mechanism for live reload, where the browser
periodically checks for file modifications and reloads when changes
are detected.
"""

import http.server
import socketserver
import threading
import webbrowser
from pathlib import Path

import markdown
from watchfiles import watch

# JavaScript for live reload via polling
LIVE_RELOAD_SCRIPT = """
<script>
(function() {
    let lastModified = 0;
    const CHECK_INTERVAL = 500;

    async function checkForUpdates() {
        try {
            const response = await fetch('/__reload__');
            const data = await response.json();
            if (lastModified > 0 && data.modified > lastModified) {
                location.reload();
            }
            lastModified = data.modified;
        } catch (e) {
            console.error('Live reload check failed:', e);
        }
    }

    setInterval(checkForUpdates, CHECK_INTERVAL);
    checkForUpdates();
})();
</script>
"""


class ResumePreviewHandler(http.server.BaseHTTPRequestHandler):
    """HTTP handler for serving resume preview with live reload.

    This handler serves the rendered resume HTML and provides a
    ``/__reload__`` endpoint for the live reload polling mechanism.

    Attributes:
        md_path: Path to the Markdown file being previewed.
        css_path: Path to the CSS stylesheet.
        modification_time: Timestamp of the most recent file modification.
    """

    md_path: Path
    css_path: Path
    modification_time: float = 0

    def log_message(self, format: str, *args: object) -> None:
        """Suppress default HTTP request logging."""
        pass

    def do_GET(self) -> None:
        """Handle GET requests.

        Routes requests to either the reload check endpoint or the
        main preview page.
        """
        if self.path == "/__reload__":
            self._handle_reload_check()
        else:
            self._serve_preview()

    def _handle_reload_check(self) -> None:
        """Return current modification timestamp as JSON.

        The browser polls this endpoint to detect file changes and
        trigger page reloads.
        """
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Cache-Control", "no-cache")
        self.end_headers()
        self.wfile.write(f'{{"modified": {self.modification_time}}}'.encode())

    def _serve_preview(self) -> None:
        """Serve the HTML preview page.

        Renders the Markdown with CSS and injects the live reload
        script for automatic refreshing.
        """
        try:
            html = self._render_html()
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Cache-Control", "no-cache")
            self.end_headers()
            self.wfile.write(html.encode("utf-8"))
        except Exception as e:
            self.send_response(500)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write(f"Error: {e}".encode())

    def _render_html(self) -> str:
        """Render the Markdown file with CSS to a complete HTML document.

        Returns:
            HTML string with embedded CSS, screen-friendly overrides,
            and the live reload script.
        """
        md_content = self.md_path.read_text(encoding="utf-8")
        css_content = self.css_path.read_text(encoding="utf-8")

        md = markdown.Markdown(
            extensions=["extra", "smarty", "sane_lists"],
            output_format="html5",
        )
        body_html = md.convert(md_content)

        # Add screen-friendly overrides for preview
        screen_css = """
        /* Screen preview overrides */
        @media screen {
            body {
                max-width: 8.5in;
                margin: 20px auto;
                padding: 0.5in 0.6in;
                background: white;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }
            html {
                background: #f0f0f0;
            }
        }
        """

        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Resume Preview - Live Reload</title>
    <style>
{css_content}
{screen_css}
    </style>
</head>
<body>
{body_html}
{LIVE_RELOAD_SCRIPT}
</body>
</html>"""


def create_handler(md_path: Path, css_path: Path) -> type[ResumePreviewHandler]:
    """Create a handler class configured with the given file paths.

    Creates a subclass of ResumePreviewHandler with the md_path and
    css_path class attributes set to the specified values.

    Args:
        md_path: Path to the Markdown file to preview.
        css_path: Path to the CSS stylesheet.

    Returns:
        A configured handler class ready for use with a TCP server.
    """

    class ConfiguredHandler(ResumePreviewHandler):
        pass

    ConfiguredHandler.md_path = md_path
    ConfiguredHandler.css_path = css_path
    ConfiguredHandler.modification_time = 0
    return ConfiguredHandler


def run_server(
    md_path: Path,
    css_path: Path,
    port: int = 8000,
    open_browser: bool = True,
) -> None:
    """Run the live-reload preview server.

    Starts an HTTP server that serves the resume preview and watches
    for file changes. When the Markdown or CSS files are modified,
    the browser automatically reloads to show the updates.

    Args:
        md_path: Path to the Markdown file to preview.
        css_path: Path to the CSS stylesheet.
        port: Port number to serve on. Defaults to 8000.
        open_browser: Whether to automatically open the preview in
            the default web browser. Defaults to True.

    Note:
        This function blocks until interrupted with Ctrl+C.

    Example:
        >>> from pathlib import Path
        >>> run_server(  # doctest: +SKIP
        ...     md_path=Path("resume.md"),
        ...     css_path=Path("assets/modern.css"),
        ...     port=8000,
        ...     open_browser=True
        ... )
        Serving resume preview at http://localhost:8000
        Press Ctrl+C to stop
    """
    handler_class = create_handler(md_path, css_path)

    # Update modification time
    def update_mod_time() -> None:
        md_mtime = md_path.stat().st_mtime if md_path.exists() else 0
        css_mtime = css_path.stat().st_mtime if css_path.exists() else 0
        handler_class.modification_time = max(md_mtime, css_mtime)

    update_mod_time()

    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", port), handler_class) as httpd:
        url = f"http://localhost:{port}"
        print(f"Serving resume preview at {url}")
        print(f"  Markdown: {md_path}")
        print(f"  CSS:      {css_path}")
        print("Press Ctrl+C to stop\n")

        if open_browser:
            webbrowser.open(url)

        # Watch for file changes in background thread
        def watch_files() -> None:
            watch_paths = [md_path.parent]
            if css_path.parent != md_path.parent:
                watch_paths.append(css_path.parent)

            for changes in watch(*watch_paths):
                for change_type, changed_path in changes:
                    changed = Path(changed_path)
                    if changed == md_path or changed == css_path:
                        update_mod_time()
                        print(f"[reload] {changed.name} modified")

        watcher_thread = threading.Thread(target=watch_files, daemon=True)
        watcher_thread.start()

        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down server...")
