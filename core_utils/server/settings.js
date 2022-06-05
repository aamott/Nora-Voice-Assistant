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


// populate settings page with data from server
function populateSettings(settings) {
    generalSettings = {};
    if (typeof settings === 'object') {
        for (let key in settings) {
            let item = settings[key];
            // if an item is a dictionary, it is a group
            if (typeof item === 'object') {
                populateSettingsGroup(key, item);
            } else {
                // add the item to the general settings array
                generalSettings[key] = item;
            }
        }

        // add general settings to the settings page
        populateSettingsGroup('General', generalSettings);
    }
}


// populate settings item
function populateSettingsGroup(key, item, parent=null, groupName='') {
    // create group
    let group = document.createElement('form');
    group.innerHTML = `<h3>${key}</h3>`;
    group.classList.add('settings-group');
    group.id = groupName + '.' + key;

    // create group items
    for (let itemKey in item) {
        if (typeof item[itemKey] === 'number') {
            // if item is an integer, make it a number input
            group.innerHTML += `<label for="${itemKey}">${itemKey}</label>
                                <input type="number" id="${itemKey}" value="${item[itemKey]}">`;
        } else  if (typeof item[itemKey] === 'boolean') {
            // if item is a boolean, make it a checkbox
            group.innerHTML += `<label for="${itemKey}">${itemKey}</label>
                                <input type="checkbox" id="${itemKey}" ${item[itemKey] ? 'checked' : ''}>`;
        } else if (Array.isArray(item[itemKey])) {
            // if an item is an array, make it a select input
            label = document.createElement('label');
            label.innerHTML = `<label for="${itemKey}">${itemKey}</label>`
            group.appendChild(label);
            select = document.createElement('select');
            select.id = itemKey;
            for (subitem of item[itemKey]) {
                select.appendChild(new Option(subitem, subitem));
            }
            group.appendChild(select);
        } else if (typeof item[itemKey] === 'object') {
            // if item is an object, recursively call this function
            populateSettingsGroup( itemKey, item[ itemKey ], group, groupName + '.' + key );
        } else if (typeof item[itemKey] === 'string' || item[itemKey] === null) {
            // if an item is a string or null, make it a text input
            group.innerHTML += `<label for="${itemKey}">${itemKey}</label>
                                <input type="text" id="${itemKey}" value="${item[itemKey]}">`;
        }
    }

    // add group to settings
    if (parent) {
        parent.appendChild(group);
    } else {
        document.getElementById('settings').appendChild(group);
    }
}


// fetch settings once page is loaded
window.addEventListener('load', fetchSettings);