Feature: Robots.txt

    Scenario: Robots.txt on claim app should disallow everything
     Given the app is running
      When we visit /robots.txt
       Then the page should include "User-agent: *"
        And the page should include "Disallow: /"

    Scenario: Robots.txt on IP app should disallow everything
     Given the IP app is running
      When we visit /robots.txt
       Then the page should include "User-agent: *"
        And the page should include "Disallow: /"
