document.addEventListener('DOMContentLoaded', () => {
    const container = document.getElementById('container');
    const registerBtn = document.getElementById('register');
    const loginBtn = document.getElementById('login');

    const loginForm = document.getElementById('login-form');
    const registerForm = document.getElementById('register-form');

    const loginError = document.getElementById('login-error');
    const regError = document.getElementById('reg-error');

    // Toggle Panels
    if (registerBtn) {
        registerBtn.addEventListener('click', () => {
            container.classList.add("active");
        });
    }

    if (loginBtn) {
        loginBtn.addEventListener('click', () => {
            container.classList.remove("active");
        });
    }

    // Traditional Register
    if (registerForm) {
        registerForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const name = document.getElementById('reg-name').value;
            const email = document.getElementById('reg-email').value;
            const password = document.getElementById('reg-password').value;

            try {
                const resp = await fetch('/api/auth/register', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ name, email, password })
                });
                const data = await resp.json();
                if (resp.ok) {
                    alert('Đăng ký thành công! Hãy đăng nhập.');
                    container.classList.remove("active");
                } else {
                    regError.innerText = data.detail || 'Lỗi đăng ký';
                }
            } catch (err) {
                regError.innerText = 'Không thể kết nối máy chủ';
            }
        });
    }

    // Traditional Login
    if (loginForm) {
        loginForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const email = document.getElementById('login-email').value;
            const password = document.getElementById('login-password').value;

            try {
                const resp = await fetch('/api/auth/login', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ email, password })
                });
                const data = await resp.json();
                if (resp.ok) {
                    window.location.href = '/';
                } else {
                    loginError.innerText = data.detail || 'Sai tài khoản hoặc mật khẩu';
                }
            } catch (err) {
                loginError.innerText = 'Không thể kết nối máy chủ';
            }
        });
    }

    // Google Login Logic
    window.handleCredentialResponse = async (response) => {
        try {
            const resp = await fetch('/api/auth/google-login', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ token: response.credential })
            });
            if (resp.ok) {
                window.location.href = '/';
            } else {
                const data = await resp.json();
                alert('Lỗi Google Login: ' + data.detail);
            }
        } catch (err) {
            console.error(err);
        }
    };

    // Official Google Wide Button Rendering
    const initGoogleIdentity = () => {
        if (typeof google !== 'undefined' && google.accounts && google.accounts.id) {
            const btnConfig = {
                type: "standard", // Đổi sang nút thanh dài có chữ
                shape: "pill",
                theme: "outline",
                size: "large",
                text: "signin_with",
                width: 300 // Chiều rộng rộng hơn để đẹp
            };

            const loginBtnDiv = document.getElementById('google-login-btn');
            const signupBtnDiv = document.getElementById('google-signup-btn');

            try {
                if (loginBtnDiv) google.accounts.id.renderButton(loginBtnDiv, btnConfig);
                if (signupBtnDiv) google.accounts.id.renderButton(signupBtnDiv, btnConfig);
                
                google.accounts.id.prompt((notification) => {
                    if (notification.isNotDisplayed()) {
                        console.log("One tap hidden: " + notification.getNotDisplayedReason());
                    }
                });
            } catch (err) {
                console.error("Google button render error:", err);
            }
        } else {
            if (!window._google_retry) window._google_retry = 0;
            if (window._google_retry < 5) {
                window._google_retry++;
                setTimeout(initGoogleIdentity, 1000);
            }
        }
    };

    initGoogleIdentity();
});
