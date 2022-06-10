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
    generalSettings.id = 'general';
    generalSettings.innerHTML = `<h2>General</h2>`;

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
 */
// Make a function that will fetch all the settings and populate the page
function initSettings(setting, settings_path='', name='', parent=null) {
    if (!setting || !parent) {
        return;
    }

    // settingElement will either be made into a group (div) or a setting (input/label)
    let settingElement = null

    // It's a settings group
    if ( setting.constructor == Object) {

        // Create group
        let group = document.createElement('div');
        group.innerHTML = `<h3>${name}</h3>`;
        group.classList.add('settings-group');
        group.id = settings_path;

        // Add group to parent
        parent.appendChild( group );

        for (key in setting) {
            // Group is passed by reference. This will add a bunch of child elements to the group.
            initSettings( setting[ key ], settings_path + '.' + key, name = key, parent = group );
        }

    // It's a setting
    } else {
        settingElement = getSettingsElement(setting, settings_path, name);

        // Add the setting to the parent
        parent.appendChild( settingElement );
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
    settingElement.id = settings_path;
    // settingElement.innerHTML = `<h3>${name}</h3>`;

    // if the setting is a number, make it a number input
    if ( typeof setting === 'number' ) {
        settingElement.innerHTML += `<label for="${settings_path}">${name}</label>
                                 <input type="number" id="${settings_path}" value="${setting}">`;

    // if the setting is a boolean, make it a checkbox
    } else if ( typeof setting === 'boolean' ) {
        settingElement.innerHTML += `<label for="${settings_path}">${name}</label>
                                 <input type="checkbox" id="${settings_path}" ${setting ? 'checked' : ''}>`;

    // if the setting is an array, make it a select input
    } else if ( Array.isArray( setting ) ) {
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


// fetch settings once page is loaded
window.addEventListener('load', fetchSettings);