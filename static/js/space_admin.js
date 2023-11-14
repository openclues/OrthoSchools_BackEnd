(function($){
    $(document).ready(function(){
        function toggleOptionalFields() {
            var allowedUserTypes = $('.allowed-user-types-field').val();
            var userTypes = ['basic_student', 'premium_student', 'blogger'];
            userTypes.forEach(function(userType) {
                var isOptionalField = $('.field-is_optional_for_' + userType);
                if (allowedUserTypes.includes(userType)) {
                    isOptionalField.show();
                } else {
                    isOptionalField.hide();
                }
            });
        }

        // Initial toggle on page load
        toggleOptionalFields();

        // Toggle on change
        $('.allowed-user-types-field').change(function() {
            toggleOptionalFields();
        });
    });
})(django.jQuery);
