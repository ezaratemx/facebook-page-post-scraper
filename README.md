# Facebook Page Post Scraper

## Running the Crawler

    1. Change the default values inside 'settings.py'.
    2. Run the crawler using ant of these 2 command line options:
    
        * Scheduled Job:
        
                python crawler_job.py --s   #This option will run the crawler as an "scheduled" job. The crawler will wait for the right schedule time set on the 'settings.py' everyday before it begin crawling.
       
        
        * Unscheduled Job:
            
                python crawler_job.py --u   #This option will run the crawler as an "unscheduled" job. The crawler will immediately run after entering the command.