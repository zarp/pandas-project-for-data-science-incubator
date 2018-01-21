Data science incubator miniproject (Fall 2016): analyzing NY restaurant inspection data

The city of New York does restaurant inspections and assigns a grade.
The file `RI_Webextract_BigApps_Latest.xls` contains a description of each of
the datafiles.  Take a look and then load the csv formatted `*.txt` files into
a database as five tables:
1. `actions`
2. `cuisines`
3. `violations`
4. `grades` (from `WebExtract.txt`)
5. `boroughs` (from `RI_Webextract_BigApps_Latest.xls`)

# Questions

##Q1: score_by_zipcode
Return a list of tuples of the form:

    (zipcode, mean score, standard error, number of restaurants)

for each of the 92 zipcodes in the city with over 100 restaurants. Use the
score from the latest inspection date for each restaurant. Sort the list in
ascending order by mean score.

**Note:** There is an interesting discussion here about what the mean score
*means* in this dataset. Think about what we're actually calculating -
does it represent what we're trying to understand about these zipcodes?

What if we use the average of a restaurant's inspections instead of the latest?

##Q2: score_by_borough
Return a list of tuples of the form:

    (borough, mean score, stderr, number of restaurants)

for each of the city's five boroughs. Sort the list in ascending order by grade.

##Q3: score_by_cuisine
Return a list of the 75 tuples of the form

    (cuisine, mean score, stderr, number of reports)

for each of the 75 cuisine types with at least 100 violation reports. Sort the
list in ascending order by score. Are the least sanitary and most sanitary
cuisine types surprising?

##Q4: violation_by_cuisine
Which cuisines tend to have a disproportionate number of what which violations?
Answering this question isn't easy becuase you have to think carefully about
normalizations.

1. More popular cuisine categories will tend to have more violations just
   becuase they represent more restaurants.
2. Similarly, some violations are more common.  For example, knowing that
   "Equipment not easily movable or sealed to floor" is a common violation for
   Chinese restuarants is not particularly helpful when it is a common
   violation for all restaurants.

The right quantity is to look at is the conditional probability of a specific
type of violation given a specific cuisine type and divide it by the
unconditional probability of the violation for the entire population. Taking
this ratio gives the right answer.  Return the 20 highest ratios of the form:

    ((cuisine, violation), ratio, count)

**Hint:**
1. The definition of a violation changes with time.  For example, 10A can mean
   two different things "Toilet facility not maintained ..." or "Vermin or
   other live animal present ..." when things were prior to 2003. To deal with
   this, you should limit your analysis to violation codes with end date after
   Jan 1, 2014. (This end date refers to the validity time ranges in
   Violation.txt).
2. The ratios don't mean much when the number of violations of a given type and
   for a specific category are not large (why not?).  Be sure to filter these
   out.  We chose 100 as our cutoff.

