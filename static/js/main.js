/**
 * Choudhary Travels — Main JavaScript
 */

document.addEventListener('DOMContentLoaded', function () {
    // Initialize AOS animations
    if (typeof AOS !== 'undefined') {
        AOS.init({
            duration: 700,
            easing: 'ease-out-cubic',
            once: true,
            offset: 60,
        });
    }

    // Auto-dismiss alerts after 5 seconds
    document.querySelectorAll('.alert-dismissible').forEach(function (alert) {
        setTimeout(function () {
            var bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
            bsAlert.close();
        }, 5000);
    });

    // Navbar shrink on scroll
    var navbar = document.querySelector('.main-nav');
    if (navbar) {
        window.addEventListener('scroll', function () {
            if (window.scrollY > 50) {
                navbar.classList.add('scrolled');
            } else {
                navbar.classList.remove('scrolled');
            }
        });
    }

    // Set minimum date on date inputs
    var today = new Date().toISOString().split('T')[0];
    document.querySelectorAll('input[type="date"]').forEach(function (input) {
        if (!input.min) {
            input.min = today;
        }
    });
    // Restrict name inputs to only alphabets, spaces, dots, hyphens, and apostrophes (prevent numbers/emojis)
    const nameInputs = document.querySelectorAll('#id_customer_name, #id_name');
    nameInputs.forEach(function (input) {
        input.addEventListener('input', function () {
            this.value = this.value.replace(/[^a-zA-Z\s.\-']/g, '');
        });
    });

    // Restrict phone inputs to only digits (0-9)
    const phoneInputs = document.querySelectorAll('#id_phone');
    phoneInputs.forEach(function (input) {
        input.addEventListener('input', function () {
            this.value = this.value.replace(/[^0-9]/g, '');
        });
    });

    // Booking form enhancements
    initBookingForm();
});

/**
 * Initialize booking form features
 */
function initBookingForm() {
    // Get form elements
    var tripTypeSelect = document.getElementById('id_trip_type');
    var returnDateField = document.getElementById('id_return_date');
    var pickupDateInput = document.getElementById('id_pickup_date');
    var returnDateInput = document.getElementById('id_return_date');

    // Hide/show return date based on trip type
    if (tripTypeSelect && returnDateField) {
        var returnCol = returnDateField.closest('.col-md-4') || returnDateField.closest('.col-12');
        function updateReturnVisibility() {
            if (tripTypeSelect.value === 'round_trip') {
                if (returnCol) returnCol.classList.remove('d-none');
                if (returnDateInput) returnDateInput.required = true;
            } else {
                if (returnCol) returnCol.classList.add('d-none');
                if (returnDateInput) returnDateInput.required = false;
            }
        }
        tripTypeSelect.addEventListener('change', updateReturnVisibility);
        updateReturnVisibility();
    }

    // Validate return date is after pickup date
    if (pickupDateInput && returnDateInput) {
        pickupDateInput.addEventListener('change', validateDates);
        returnDateInput.addEventListener('change', validateDates);
    }

    function validateDates() {
        var pickupDate = pickupDateInput.value;
        var returnDate = returnDateInput.value;
        if (pickupDate && returnDate) {
            if (returnDate <= pickupDate) {
                returnDateInput.classList.add('is-invalid');
                returnDateInput.addEventListener('focus', function () {
                    this.classList.remove('is-invalid');
                });
            }
        }
    }

    // Initialize price calculator if vehicle data exists
    initPriceCalculator();
}

/**
 * Initialize real-time price calculator
 */
function initPriceCalculator() {
    var vehicleSelect = document.getElementById('id_vehicle');
    var priceDisplay = document.getElementById('price-estimate');

    if (!vehicleSelect || !priceDisplay) return;

    // Store vehicle data from select options
    var vehicleData = {};
    document.querySelectorAll('#id_vehicle option').forEach(function (option) {
        if (option.value) {
            vehicleData[option.value] = {
                name: option.text,
                price_per_km: parseFloat(option.getAttribute('data-price-per-km')) || 0,
                price_per_day: parseFloat(option.getAttribute('data-price-per-day')) || 0,
            };
        }
    });

    // Calculate and display price on form changes
    var pickupDate = document.getElementById('id_pickup_date');
    var returnDate = document.getElementById('id_return_date');
    var tripType = document.getElementById('id_trip_type');

    function calculatePrice() {
        if (!vehicleSelect.value) {
            priceDisplay.innerHTML = '<span class="text-muted">Select a vehicle</span>';
            return;
        }

        var pickup = pickupDate ? pickupDate.value : '';
        var dropoff = returnDate ? returnDate.value : '';
        var trip = tripType ? tripType.value : 'one_way';
        var vehicle = vehicleData[vehicleSelect.value];

        if (!pickup) {
            priceDisplay.innerHTML = '<span class="text-muted">Select pickup date</span>';
            return;
        }

        var pickupDateTime = new Date(pickup + 'T00:00:00');
        var days = 0;

        if (trip === 'round_trip' && dropoff) {
            var returnDateTime = new Date(dropoff + 'T00:00:00');
            days = Math.ceil((returnDateTime - pickupDateTime) / (1000 * 60 * 60 * 24));
        } else {
            days = 1;
        }

        if (days < 1) days = 1;

        // For simplicity, use price_per_day
        var estimatedPrice = vehicle.price_per_day * days;

        priceDisplay.innerHTML = '₹<strong>' + estimatedPrice.toLocaleString('en-IN') + '</strong> (approx.)';
    }

    if (vehicleSelect) vehicleSelect.addEventListener('change', calculatePrice);
    if (pickupDate) pickupDate.addEventListener('change', calculatePrice);
    if (returnDate) returnDate.addEventListener('change', calculatePrice);
    if (tripType) tripType.addEventListener('change', calculatePrice);

    // Initial calculation
    calculatePrice();
}