Feature: claimants contact details

    Scenario: capturing claimants contact details so that they can be contacted by RPS
        Given the app is running
         When we visit the /claimant-contact-details page
         Then the page should have title "Claimant Contact Details"
          And the page should have an input field called "forenames" labeled "Forename(s)"
          And the page should have an input field called "surname" labeled "Surname"