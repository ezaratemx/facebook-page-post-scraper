import schedule
import time
import get_fb_posts_fb_group,get_fb_posts_fb_page,get_fb_comments_from_fb
import settings
from threading import Thread
import sys,getopt
from optparse import OptionParser

def main(argv):

    parser = OptionParser()
    parser.add_option("--s", action="store_true", dest="scheduled")
    parser.add_option("--u", action="store_true", dest="unscheduled")
    (options, args) = parser.parse_args()
    if not options.scheduled and not options.unscheduled:
        scheduled_job_start()
    else:
        if options.scheduled:
            scheduled_job_start()
        elif options.unscheduled:
            unscheduled_job_start()



def scheduled_job_start():
    print 'Wating for time schedule at ({0}). . .'.format(settings.schedule_time)
    schedule.every().day.at(settings.schedule_time).do(job)
    while True:
        schedule.run_pending()
        time.sleep(1)

def unscheduled_job_start():
    job()

def job():
    reload(settings)
    print ('Crawling has been started. . .')
    get_fb_posts_fb_group.reset_deleted_tag()
    get_fb_posts_fb_page.reset_deleted_tag()
    get_fb_comments_from_fb.reset_deleted_tag()
    Thread(target=group_posts_job).start()
    Thread(target=page_posts_job).start()



def group_posts_job():
    for sgroup_id in settings.group_id_for_posts:
        get_fb_posts_fb_group.work_as_scheduled(sgroup_id)
        get_fb_comments_from_fb.work_as_scheduled(sgroup_id)

def page_posts_job():
    for spage_id in settings.page_id_for_posts:
        get_fb_posts_fb_page.work_as_scheduled(spage_id)
        get_fb_comments_from_fb.work_as_scheduled(spage_id)



if __name__ == "__main__":
   main(sys.argv[1:])