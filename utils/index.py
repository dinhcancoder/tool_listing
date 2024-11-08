def show_toast(page, message, toast_type="success"):
    background_color = "#009995" if toast_type == "success" else "#FF4C4C"
    
    js_code = f"""
    (() => {{
        let container = document.getElementById('custom-toast-container');
        if (!container) {{
            container = document.createElement('div');
            container.id = 'custom-toast-container';
            container.style.position = 'fixed';
            container.style.top = '10px';
            container.style.right = '10px';
            container.style.zIndex = '10000';
            container.style.display = 'flex';
            container.style.flexDirection = 'column';
            container.style.gap = '10px';
            document.body.appendChild(container);
        }}

        const toast = document.createElement('div');
        toast.className = 'custom-toast';
        toast.style.background = "{background_color}";
        toast.style.color = "#fff";
        toast.style.padding = "11px 25px";
        toast.style.borderRadius = "5px";
        toast.style.boxShadow = "0px 4px 6px rgba(0, 0, 0, 0.1)";
        toast.style.fontSize = "14px";
        toast.style.maxWidth = "300px";
        toast.style.opacity = "1";
        toast.style.transition = "opacity 0.5s";
        toast.textContent = "{message}";

        container.appendChild(toast);

        setTimeout(() => {{
            toast.style.opacity = "0";
            setTimeout(() => toast.remove(), 500);
        }}, 4000);
    }})();
    """
    page.evaluate(js_code)
