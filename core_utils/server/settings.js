//----------------------------------------------
// Settings.js
// Populates and manages the settings page.
//----------------------------------------------

// fetch settings json from server endpoint '/settings'
function fetchSettings() {
    fetch('/settings')
        .then(response => response.json())
        .then(settings => populateSettings(settings))
        .catch(error => console.error('Error:', error));
}


/**
 * @param {Object} settings 
 */
// populate settings page with data from server
function populateSettings(settings) {
    main_page = document.getElementById( 'settings' );

    // make a group for the first level of settings
    let generalSettings = document.createElement( 'section' );
    generalSettings.className = 'settings-group';
    generalSettings.id = 'general-settings';
    generalSettings.innerHTML = `<h2>General</h2>`;
    generalSettings.settingsPath = '';

    for (key in settings) {
        if ( !key ) {
            continue;
        }
        // if key is a group, create a new section
        if ( settings[key].constructor == Object ) {
            initSettings( settings[ key ], settings_path = key, name = key, parent = main_page );
        // if key is a setting, create a new setting and append it to the general settings element
        } else {
            settingElement = getSettingsElement(settings[ key ], name=key);
            generalSettings.appendChild(settingElement);
        }
    }

    // add generalSettings to the settings page
    main_page.appendChild( generalSettings );
}


/**
 * 
 * @param {Object} setting 
 * @param {string} settings_path 
 * @param {string} name 
 * @param {HTMLElement} parent 
 * @returns {[HTMLElement, bool]} html element, is element a group
 */
// Make a function that will fetch all the settings and populate the page
function initSettings(setting, settings_path='', name='', parent=null) {
    const IS_GROUP = true;
    const IS_SETTING = false;

    if (!setting || !parent) {
        return [null, IS_GROUP];
    }

    // settingElement will either be made into a group (div) or a setting (input/label)
    let settingElement = null

    // It's a settings group
    if ( setting.constructor == Object) {

        // Create group
        let group = document.createElement('div');
        group.innerHTML = `<h3>${name}</h3>`;
        group.classList.add('settings-group');
        // group.id = settings_path;

        // Add group to parent
        parent.appendChild( group );

        // Stores the elements for a form at the end of the group
        let form_elements = [];

        for (key in setting) {
            // Group is passed by reference. This will add a bunch of child elements to the group.
            let element, is_group;
            [element, is_group] = initSettings( setting[ key ], settings_path + '.' + key, /*name*/ key, /*parent*/ group );

            // only add the element to the form if it's not a group
            if ( !is_group && typeof element === 'object' ) {
                form_elements.push( element );
            }
        }

        // Add all the elements to a form if there are any
        if ( form_elements.length > 0 ) {
            let form = document.createElement('form');
            form.classList.add('settings-form');
            form.id = settings_path;
            form.settingsPath = settings_path;
            
            // Add all the elements to the form
            for (element of form_elements) {
                form.appendChild( element );
            }

            // submit button
            form.innerHTML += `<button type='button' onclick='saveSettings("${form.id}")'>Save</button>`;


            // Add the form to the group
            group.appendChild( form );
        }


        return [group, IS_GROUP];

    // It's a setting
    } else {
        settingElement = getSettingsElement(setting, settings_path, name);
        return [settingElement, IS_SETTING];
    }
}


/**
 * 
 * @param {Object} setting 
 * @param {string} settings_path 
 * @param {string} name 
 * @returns {HTMLElement}
 */
function getSettingsElement(setting, settings_path='', name='') {
    // Create a new element for the setting
    let settingElement = document.createElement( 'div' );
    settingElement.classList.add( 'setting' );
    settingElement.id = settings_path + '.' + name + '-parent';
    // settingElement.innerHTML = `<h3>${name}</h3>`;

    // if the setting is a number, make it a number input
    if ( typeof setting === 'number' ) {
        // TODO: is settings_path the path to the entire setting, or do we need to add the name to the path?
        settingElement.innerHTML += `<label for="${settings_path}">${name}</label>
                                 <input type="number" id="${settings_path}" value="${setting}">`;

    // if the setting is a boolean, make it a checkbox
    } else if ( typeof setting === 'boolean' ) {
        settingElement.innerHTML += `<label for="${settings_path}">${name}</label>
                                 <input type="checkbox" id="${settings_path}" ${setting ? 'checked' : ''}>`;

    // if the setting is an array, make it a select input
    } else if ( Array.isArray( setting ) ) {
        // TODO: Try replacing the settingElement with the select input instead of appending it
        // create a label for the select
        label = document.createElement( 'label' );
        label.innerHTML = `<label for="${settings_path}">${name}</label>`
        settingElement.appendChild( label );

        // create a select element
        select = document.createElement( 'select' );
        select.id = settings_path;
        for ( subitem of setting ) {
            select.appendChild( new Option( subitem, subitem ) );
        }
        settingElement.appendChild( select );
    
    // if the setting is a string or null, make it a text input
    } else if ( typeof setting === 'string' || setting === null ) {
        settingElement.innerHTML += `<label for="${settings_path}">${name}</label>
                                 <input type="text" id="${settings_path}" value="${setting}">`;
    }
    
    return settingElement;
}



// Function to save settings in a specific form to server
function saveSettings(formId) {
    let form = document.getElementById(formId);
    let settings_path = form.settingsPath;
    let settings = {};

    // Get all the inputs in the form
    let inputs = form.getElementsByTagName('input');
    for (input of inputs) {
        // if the input is a checkbox, get the value as a boolean
        if ( input.type === 'checkbox' ) {
            settings[input.id] = input.checked;
        }
        // if the input is a number, get the value as a number
        else if ( input.type === 'number' ) {
            settings[input.id] = parseInt(input.value);
        }
        // if the input is a text input, get the value as a string
        else if ( input.type === 'text' ) {
            settings[input.id] = input.value;
        }
        // if the input is a select input, get the value as a string
        else if ( input.type === 'select-one' ) {
            settings[input.id] = input.value;
        }
    }

    // Get all the textareas in the form
    let textareas = form.getElementsByTagName('textarea');
    for (textarea of textareas) {
        settings[textarea.id] = textarea.value;
    }

    // Get all the selects in the form
    let selects = form.getElementsByTagName('select');
    for (select of selects) {
        settings[select.id] = select.value;
    }

    // Send the settings to the server
    sendSettings(settings_path, settings);
}


// Function to send settings to the server
function sendSettings(settings_path, settings) {
    // Send the settings to the server one by one
    for (key in settings) {
        let setting = settings[key];
        let setting_path = settings_path + '.' + key;
        sendSetting(setting_path, setting);
    }
}


// Function to send a single setting to the server
function sendSetting(setting_path, setting) {
    // // convert the setting to a JSON string
    let setting_json = JSON.stringify( {value: setting} );

    // send the setting to the server
    let xhr = new XMLHttpRequest();
    xhr.open('POST', '/settings/' + setting_path, true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.send( setting_json );
}

    

// fetch settings once page is loaded
window.addEventListener('load', fetchSettings);