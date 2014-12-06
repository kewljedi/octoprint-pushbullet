$(function() {
    function PushbulletViewModel(parameters) {
        var self = this;

        self.loginState = parameters[0];
        self.settingsViewModel = parameters[1];

        self.onBeforeBinding = function() {
            self.settings = self.settingsViewModel.settings;
        };

        self.onSettingsShown = function() {
            self.requestData();
        };

    }

    // view model class, parameters for constructor, container to bind to
    ADDITIONAL_VIEWMODELS.push([PushbulletViewModel, ["loginStateViewModel", "settingsViewModel"], document.getElementById("settings_plugin_pushbullet_dialog")]);
});