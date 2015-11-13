############################################################
# Course scheduling specifics.

# Information about a course:
# - self.cid: course ID (e.g., CS221)
# - self.name: name of the course (e.g., Artificial Intelligence)
# - self.quarters: quarters without the years (e.g., Aut)
# - self.minUnits: minimum allowed units to take this course for (e.g., 3)
# - self.maxUnits: maximum allowed units to take this course for (e.g., 3)
# - self.prereqs: list of course IDs that must be taken before taking this course.
class Course:
    def __init__(self, info):
        self.__dict__.update(info)

    # Return whether this course is offered in |quarter| (e.g., Aut2013).
    def is_offered_in(self, quarter):
        return any(quarter.startswith(q) for q in self.quarters)

    def short_str(self): return '%s: %s' % (self.cid, self.name)

    def __str__(self):
        return 'Course{cid: %s, name: %s, quarters: %s, units: %s-%s, prereqs: %s}' % (self.cid, self.name, self.quarters, self.minUnits, self.maxUnits, self.prereqs)


# Information about all the courses
class CourseBulletin:
    def __init__(self, coursesPath):
        """
        Initialize the bulletin.

        @param coursePath: Path of a file containing all the course information.
        """
        # Read courses (JSON format)
        self.courses = {}
        info = json.loads(open(coursesPath).read())
        for courseInfo in info.values():
            course = Course(courseInfo)
            self.courses[course.cid] = course

# A request to take one of a set of courses at some particular times.
class Request:
    def __init__(self, cids, quarters, prereqs, weight):
        """
        Create a Request object.

        @param cids: list of courses from which only one is chosen.
        @param quarters: list of strings representing the quarters (e.g. Aut2013)
            the course must be taken in.
        @param prereqs: list of strings representing courses pre-requisite of
            the requested courses separated by comma. (e.g. CS106,CS103,CS109)
        @param weight: real number denoting how much the student wants to take
            this/or one the requested courses.
        """
        self.cids = cids
        self.quarters = quarters
        self.prereqs = prereqs
        self.weight = weight

    def __str__(self):
        return 'Request{%s %s %s %s}' % \
            (self.cids, self.quarters, self.prereqs, self.weight)

    def __eq__(self, other): return str(self) == str(other)

    def __cmp__(self, other): return cmp(str(self), str(other))

    def __hash__(self): return hash(str(self))

    def __repr__(self): return str(self)

# Given the path to a preference file and a
class Profile:
    def __init__(self, bulletin, prefsPath):
        """
        Parses the preference file and generate a student's profile.

        @param prefsPath: Path to a txt file that specifies a student's request
            in a particular format.
        """
        self.bulletin = bulletin

        # Read preferences
        self.minUnits = 9  # minimum units per quarter
        self.maxUnits = 12 # maximum units per quarter
        self.quarters = [] # (e.g., Aut2013)
        self.taken = set()  # Courses that we've taken
        self.requests = []
        for line in open(prefsPath):
            m = re.match('(.*)\\s*#.*', line)
            if m: line = m.group(1)
            line = line.strip()
            if len(line) == 0: continue

            # Units
            m = re.match('minUnits (.+)', line)
            if m:
                self.minUnits = int(m.group(1))
                continue
            m = re.match('maxUnits (.+)', line)
            if m:
                self.maxUnits = int(m.group(1))
                continue

            # Register a quarter (quarter, year)
            m = re.match('register (.+)', line)
            if m:
                quarter = m.group(1)
                m = re.match('(Aut|Win|Spr|Sum)(\d\d\d\d)', quarter)
                if not m:
                    raise Exception("Invalid quarter '%s', want something like Spr2013" % quarter)
                self.quarters.append(quarter)
                continue

            # Already taken a course
            m = re.match('taken (.+)', line)
            if m:
                cid = self.ensure_course_id(m.group(1))
                self.taken.add(cid)
                continue

            # Request to take something
            # also match & to parse MS&E courses correctly
            m = re.match('request ([\w&]+)(.*)', line)
            if m:
                cids = [self.ensure_course_id(m.group(1))]
                quarters = []
                prereqs = []
                weight = 1  # Default: would want to take
                args = m.group(2).split()
                for i in range(0, len(args), 2):
                    if args[i] == 'or':
                        cids.append(self.ensure_course_id(args[i+1]))
                    elif args[i] == 'after':  # Take after a course
                        prereqs = [self.ensure_course_id(c) for c in args[i+1].split(',')]
                    elif args[i] == 'in':  # Take in a particular quarter
                        quarters = [self.ensure_quarter(q) for q in args[i+1].split(',')]
                    elif args[i] == 'weight':  # How much is taking this class worth
                        weight = float(args[i+1])
                    elif args[i].startswith('#'): # Comments
                        break
                    else:
                        raise Exception("Invalid arguments: %s" % args)
                self.requests.append(Request(cids, quarters, prereqs, weight))
                continue

            raise Exception("Invalid command: '%s'" % line)

        # Determine any missing prereqs and validate the request.
        self.taken = set(self.taken)
        self.taking = set()

        # Make sure each requested course is taken only once
        for req in self.requests:
            for cid in req.cids:
                if cid in self.taking:
                    raise Exception("Cannot request %s more than once" % cid)
            self.taking.update(req.cids)

        # Make sure user-designated prerequisites are requested
        for req in self.requests:
            for prereq in req.prereqs:
                if prereq not in self.taking:
                    raise Exception("You must take " + prereq)

        # Add missing prerequisites if necessary
        for req in self.requests:
            for cid in req.cids:
                course = self.bulletin.courses[cid]
                for prereq_cid in course.prereqs:
                    if prereq_cid in self.taken:
                        continue
                    elif prereq_cid in self.taking:
                        if prereq_cid not in req.prereqs:
                            req.prereqs.append(prereq_cid)
                            print "INFO: Additional prereqs inferred: %s after %s" % \
                                (cid, prereq_cid)
                    else:
                        print "WARNING: missing prerequisite of %s -- %s; you should add it as 'taken' or 'request'" %  \
                            (cid, self.bulletin.courses[prereq_cid].short_str())

    def print_info(self):
        print "Units: %d-%d" % (self.minUnits, self.maxUnits)
        print "Quarter: %s" % self.quarters
        print "Taken: %s" % self.taken
        print "Requests:"
        for req in self.requests: print '  %s' % req

    def ensure_course_id(self, cid):
        if cid not in self.bulletin.courses:
            raise Exception("Invalid course ID: '%s'" % cid)
        return cid

    def ensure_quarter(self, quarter):
        if quarter not in self.quarters:
            raise Exception("Invalid quarter: '%s'" % quarter)
        return quarter