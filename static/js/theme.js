    // Проверяем сохраненную тему или используем 'auto' по умолчанию
    const savedTheme = localStorage.getItem('theme') || 'auto';

    // Функция установки темы
    function setTheme(theme) {
        document.documentElement.setAttribute('data-bs-theme', theme);
        localStorage.setItem('theme', theme); // Сохраняем выбор
    }

    // Устанавливаем сохраненную тему при загрузке страницы
    setTheme(savedTheme);

    // Находим все кнопки переключателя
    document.querySelectorAll('[data-bs-theme-value]').forEach(button => {
        button.addEventListener('click', () => {
            const theme = button.getAttribute('data-bs-theme-value');
            setTheme(theme);
        });
    });