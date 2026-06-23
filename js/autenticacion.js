// ==========================================
// SECCIÓN DE LOGIN (Solo se ejecuta en login.html)
// ==========================================
const togglePasswordBtn = document.getElementById('togglePassword');
const loginForm = document.getElementById('loginForm');

if (togglePasswordBtn) {
    togglePasswordBtn.addEventListener('click', function () {
        const passwordInput = document.getElementById('password');
        if (passwordInput.type === 'password') {
            passwordInput.type = 'text';
            this.textContent = '🔒 Ocultar';
        } else {
            passwordInput.type = 'password';
            this.textContent = '👁️ Ver';
        }
    });
}

if (loginForm) {

    loginForm.addEventListener('submit', function(e) {

        e.preventDefault();

        const email = document.getElementById('email').value.trim();
        const password = document.getElementById('password').value.trim();

        if (!email || !password) {
            showError('Completa todos los campos');
            return;
        }

        fetch('/api/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                correo: email,
                password: password
            })
        })

        .then(response => response.json())

        .then(data => {

            if (data.success) {

                localStorage.setItem(
                    'usuarioLogueado',
                    'true'
                );

                localStorage.setItem(
                    'nombreUsuario',
                    data.nombre
                );

                localStorage.setItem(
                    'rolUsuario',
                    data.rol
                );

                window.location.href = '/';

            } else {

                showError(data.message);
            }

        })

        .catch(error => {

            console.error(error);

            showError(
                'Error al conectar con el servidor'
            );
        });

    });

}

function showError(message) {
    const errorDiv = document.getElementById('errorMessage');
    errorDiv.textContent = message;
    errorDiv.classList.remove('hidden');
}

// ==========================================
// SECCIÓN DE REGISTRO (Solo se ejecuta en registro.html)
// ==========================================
const registerForm = document.getElementById('registerForm');

if (registerForm) {
    registerForm.addEventListener('submit', function (e) {
        e.preventDefault();

        const fullName = document.getElementById('fullName').value.trim();
        const email = document.getElementById('email').value.trim();
        const password = document.getElementById('password').value.trim();
        const confirmPassword = document.getElementById('confirmPassword').value.trim();

        const errorDiv = document.getElementById('errorMessage');
        const successDiv = document.getElementById('successMessage');

        errorDiv.classList.add('hidden');
        successDiv.classList.add('hidden');
        errorDiv.textContent = '';
        successDiv.textContent = '';

        if (!fullName || !email || !password || !confirmPassword) {
            showRegisterError('Por favor, completa todos los campos.');
            return;
        }

        if (password.length < 6) {
            showRegisterError('La contraseña debe tener al menos 6 caracteres.');
            return;
        }

        if (password !== confirmPassword) {
            showRegisterError('Las contraseñas no coinciden. Verifica que estén escritas igual.');
            return;
        }

        // 💾 GUARDAR EL NUEVO USUARIO EN LOCALSTORAGE
        // 1. Traemos los usuarios que ya existan en el "almacén"
       const submitBtn = registerForm.querySelector('button[type="submit"]');
submitBtn.disabled = true;
submitBtn.textContent = 'Creando cuenta...';

fetch('/api/registro', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({
        nombre: fullName,
        correo: email,
        password: password
    })
})
.then(response => response.json())
.then(data => {

    if (data.success) {

        successDiv.textContent =
            '¡Cuenta creada con éxito! Redirigiendo...';

        successDiv.classList.remove('hidden');

        registerForm.reset();

        setTimeout(() => {
            window.location.href = '/login';
        }, 2000);

    } else {

        showRegisterError(data.message);

        submitBtn.disabled = false;
        submitBtn.textContent = 'Registrarse';
    }

})
.catch(error => {

    console.error(error);

    showRegisterError(
        'Error al conectar con el servidor'
    );

    submitBtn.disabled = false;
    submitBtn.textContent = 'Registrarse';
});
    });
}

function showRegisterError(message) {
    const errorDiv = document.getElementById('errorMessage');
    errorDiv.textContent = message;
    errorDiv.classList.remove('hidden');
}