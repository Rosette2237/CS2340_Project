def calculate_match(job, profile):
    if not job or not profile:
        return 0

    job_skills = {skill.strip().lower() for skill in job.split(",")}
    profile_skills = {skill.strip().lower() for skill in profile.split(",")}

    if not job_skills:
        return 0

    matches = 0
    for skill in job_skills:
        if skill in profile_skills:
            matches += 1

    return (matches / len(job_skills)) * 100
