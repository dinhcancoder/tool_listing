def show_toast_notification(page, message):
    page.evaluate(f"""
        (message => {{
            const toast = document.createElement('div');
            toast.textContent = message;
            toast.style.position = 'fixed';
            toast.style.bottom = '20px';
            toast.style.right = '20px';
            toast.style.padding = '10px';
            toast.style.backgroundColor = '#ff4d4f';
            toast.style.color = 'white';
            toast.style.borderRadius = '5px';
            toast.style.zIndex = '1000';
            document.body.appendChild(toast);

            setTimeout(() => toast.remove(), 3000);
        }}))(message);
    """)