document.addEventListener('DOMContentLoaded', function() {
    // Modal functionality
    const modals = document.querySelectorAll('.modal');
    const modalTriggers = document.querySelectorAll('[data-modal]');
    const modalClosers = document.querySelectorAll('[data-close-modal], .close-modal');

    // Open modal
    modalTriggers.forEach(trigger => {
        trigger.addEventListener('click', () => {
            const modalId = trigger.getAttribute('data-modal');
            const modal = document.getElementById(modalId);
            if (modal) {
                modal.classList.add('active');
                document.body.style.overflow = 'hidden';
            }
        });
    });

    // Close modal
    modalClosers.forEach(closer => {
        closer.addEventListener('click', () => {
            const modal = closer.closest('.modal');
            if (modal) {
                modal.classList.remove('active');
                document.body.style.overflow = '';
            }
        });
    });

    // Close modal on outside click
    modals.forEach(modal => {
        modal.addEventListener('click', (e) => {
            if (e.target === modal) {
                modal.classList.remove('active');
                document.body.style.overflow = '';
            }
        });
    });

    // Form validation and submission
    const organizationForm = document.querySelector('.organization-form');
    if (organizationForm) {
        organizationForm.addEventListener('submit', function(e) {
            const requiredFields = organizationForm.querySelectorAll('[required]');
            let isValid = true;

            requiredFields.forEach(field => {
                if (!field.value.trim()) {
                    isValid = false;
                    field.classList.add('error');
                } else {
                    field.classList.remove('error');
                }
            });

            if (!isValid) {
                e.preventDefault();
                alert('Por favor, completa todos los campos requeridos.');
            }
        });
    }

    // Organization cards hover effect
    const orgCards = document.querySelectorAll('.organization-card');
    orgCards.forEach(card => {
        card.addEventListener('mouseenter', () => {
            card.style.transform = 'translateY(-4px)';
        });

        card.addEventListener('mouseleave', () => {
            card.style.transform = 'translateY(0)';
        });
    });

    // Areas de trabajo validation
    const areasCheckboxes = document.querySelectorAll('input[name="areas[]"]');
    if (areasCheckboxes.length > 0) {
        const validateAreas = () => {
            const checkedAreas = document.querySelectorAll('input[name="areas[]"]:checked');
            if (checkedAreas.length === 0) {
                alert('Por favor, selecciona al menos un área de trabajo.');
                return false;
            }
            return true;
        };

        organizationForm.addEventListener('submit', function(e) {
            if (!validateAreas()) {
                e.preventDefault();
            }
        });
    }

    // Teléfono validation
    const phoneInput = document.getElementById('telefono');
    if (phoneInput) {
        phoneInput.addEventListener('input', function(e) {
            let value = e.target.value.replace(/\D/g, '');
            if (value.length > 10) {
                value = value.slice(0, 10);
            }
            e.target.value = value;
        });
    }
}); 