//form data to be changed
let fantasy_language_select = document.getElementById('id_fantasy_language_select');
let real_language_select = document.getElementById('id_real_language_influences');
let more_of_charfield = document.getElementById('id_more_of');
let less_of_charfield = document.getElementById('id_less_of');
let none_of_charfield = document.getElementById('id_none_of');

//populate fields based on predefined templates - for some reason onChange doesn't work so it's a whole event listener
fantasy_language_select.addEventListener("change", function() {
    let fantasy_language = String(fantasy_language_select.value.toLowerCase());
    
    //javascript presently has no method to parse json from a local file so an object needs to be created here
    fantasy_language_data = {
        "fantasy_languages": 
        {
            "orcish": {
                "long_name": "Orcish",
                "influences": ["russian", "swahili"],
                "more_of": ["g", "k", "r"],
                "less_of": ["w", "v", "y"],
                "none_of": []
            },
            "elvish": {
                "long_name": "Elvish",
                "influences": ["french", "italian"],
                "more_of": ["v"],
                "less_of": ["k", "r"],
                "none_of": []
            },
            "dwarvish": {
                "long_name": "Dwarvish",
                "influences": ["danish", "german", "swedish"],
                "more_of": ["b", "r"],
                "less_of": ["z"],
                "none_of": []
            },
            "halfling": {
                "long_name": "Halfling",
                "influences": ["spanish", "danish"],
                "more_of": ["f", "l"],
                "less_of": ["k"],
                "none_of": []
            },
            "goblin": {
                "long_name": "Goblin",
                "influences": ["spanish", "portuguese"],
                "more_of": ["z", "k", "t"],
                "less_of": [],
                "none_of": ["w"]
            },
            "gnomish": {
                "long_name": "Gnomish",
                "influences": ["spanish", "swedish", "italian"],
                "more_of": ["l", "x", "u"],
                "less_of": [],
                "none_of": []
            }
        }
    }
    //condense data object
    fantasy_language_data = fantasy_language_data.fantasy_languages

    //set values based on user's template selection
    for (let i = 0; i < real_language_select.length; i++) {
        if (fantasy_language_data[fantasy_language].influences.includes(real_language_select.options[i].value)) {//select values that match dataset
            real_language_select.options[i].selected = 1
        } else { //deselect all other values
            real_language_select.options[i].selected = 0
        }
        //real_language_select.options.selected = String(fantasy_language_data[fantasy_language].influences[i])
    }
    more_of_charfield.value = String(fantasy_language_data[fantasy_language].more_of).replace(/,/g,"")
    less_of_charfield.value = String(fantasy_language_data[fantasy_language].less_of).replace(/,/g,"")
    none_of_charfield.value = String(fantasy_language_data[fantasy_language].none_of).replace(/,/g,"")
})

