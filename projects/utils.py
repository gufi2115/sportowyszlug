from .models import ProjectM, RanksM, ReviewM
import pytz
import datetime

def ranksystem(owner_project):
    owner_projects = ProjectM.objects.filter(owner_id=owner_project)
    projects = ProjectM.objects.all()
    projects_count = ProjectM.objects.all().count()
    user_votes = []
    rank_data = []
    owner_time = []
    users_time = []
    votes_up = 0
    votes_down = 0
    votes_up_percent = 0
    all_votes = ReviewM.objects.all()
    all_votes_count = ReviewM.objects.all().count()
    # all_votes_up = ReviewM.objects.filter(value='up')
    # all_votes_down = ReviewM.objects.filter(value='down')
    projects_with_votes = []

    for project in projects:
        users_time.append(project.time)

    users_time = sum(users_time)

    for vote in all_votes:
        if vote.project_id not in projects_with_votes:
            projects_with_votes.append(vote.project_id)

    for project in owner_projects:
        reviews = ReviewM.objects.filter(project_id=project.id)
        owner_time.append(project.time)
        for review in reviews:
            user_votes.append(review.value)

    if len(owner_time) > 0:
        owner_time = min(owner_time)

    for vote_value in user_votes:
        if vote_value == 'up':
            votes_up += 1
        elif vote_value == 'down':
            votes_down += 1

    if len(user_votes) > 0:
        votes_up_percent = int(votes_up /len(user_votes) * 100)
    else:
        votes_up_percent = 0

    if len(projects_with_votes) > 0 :
        average_votes = int(all_votes_count / len(projects_with_votes))
    else:
        average_votes = 0

    average_time = int(users_time / projects_count)

    if len(user_votes) >= 3 and votes_up_percent < 40:
        rank_data.clear()
        rank_data.append('silver1.png_silver1')

    elif len(user_votes) >= 3 and 40 <= votes_up_percent < 50:
        rank_data.clear()
        rank_data.append('silver4.png_silver2')

    elif 3 <= len(user_votes) < average_votes / 2 and 50 <= votes_up_percent:
        rank_data.clear()
        rank_data.append('gold4.png_gold')

    elif len(user_votes) >= 3 and 55 <= votes_up_percent < 70 and len(user_votes) >= average_votes / 2:
        rank_data.clear()
        rank_data.append('kalach.png_kalach')

    elif len(user_votes) >= 3 and 70 <= votes_up_percent < 80 and len(user_votes) >= average_votes / 2:
        rank_data.clear()
        rank_data.append('sherif.png_sherif')

    elif len(user_votes) >= 3 and 80 <= votes_up_percent < 90 and len(user_votes) >= average_votes / 2 and owner_time <= average_time:
        rank_data.clear()
        rank_data.append('supreme.png_supreme')

    elif len(user_votes) >= 3 and 90 <= votes_up_percent and len(user_votes) >= average_votes / 2 and owner_time <= average_time:
        rank_data.clear()
        rank_data.append('global.png_global')

    return rank_data


def time_for_verification(profileObj):
    user_join_time = profileObj.created
    utc = pytz.timezone("Europe/Warsaw")
    time_now = datetime.datetime.now(utc)
    time_to_verification = datetime.timedelta(minutes=10)
    time_zone = time_now.strftime('%z')
    for time_difference in time_zone:
        if time_difference.isalnum():
            if int(time_difference) > 0:
                time_zone = int(time_difference)
    time_to_verification_user = user_join_time + time_to_verification
    difference_t = (time_to_verification_user - time_now) - datetime.timedelta(hours=time_zone)
    return difference_t