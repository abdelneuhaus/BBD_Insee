import psycopg2 # Python SQL driver for PostgreSQL
import sys

def display_dragon(prenom_dragon):
    # Try to connect to an existing database
    print('Trying to connect to the database')
    try:
       	# the method psycopg2.connect() is used to connect to a database server. 
	# Once the connection is established, psycopg2.connect() returns a connection object 
	# assigned to the variable conn 
      conn = psycopg2.connect("host=dbserver dbname=USERNAME user=USERNAME")
      print('Connected to the database')

	# the connection object contains a cursor object returned by te method conn.cursor()
	# and assigned to the variable cur. You can use cur.execute() to execute Python SQL queries on your PostgreSQL database.
      cur = conn.cursor()

      	#NEVER NEVER concatenates strings to build a SQL query
       	#see http://initd.org/psycopg/docs/usage.html#passing-parameters-to-sql-queries

	# cur.execute() is used to execute a placeholder-based query.
	# we will pass two variables to cur.execute(): 
	# command (with one placeholder %s) and param (a tuple containing a single value) 
      command = 'select * from dragons where dragon = %s'
      param = [prenom_dragon]
      print('Trying to execute command: ',command, 'with parameters: ', param )
      try:
        # Query the database and obtain data as Python objects
        cur.execute(command, param)
        print("execute ok")

        # retrieve the tuple concerning our dragon:
	# the method cur.fetchall() returns a list of tuples 	
	# each tuple corresponds to a row of the query result set
        rows = cur.fetchall() #rows => list (query results) of tuples (the selected 						attributes) 
        print("fetch ok")

        if(not rows):
            print("No dragons found") # if rows is empty
            return
        dragon = rows[0] #there is only one dragon (one result)

        result = prenom_dragon
        if dragon[1] == 'M': #check sexe attribute
          result = result + ' est un male'
        else:
          result = result + 'est une femelle'
          result = result + ' et a ' + str(dragon[2]) + ' ecailles.\n' #check nb_ecaille

        # Close communication with the database
        cur.close()
        conn.close()

	 # print the result
        print('Answer: ' + result)
        return result
      except Exception as e :
        return "error when running command: " + command + " : " + str(e)
    except Exception as e :
      return "Cannot connect to database: " + str(e)


if(len(sys.argv)==1):
    print("Usage: ", sys.argv[0], " NomDragon")
else:
    # function call
    display_dragon(sys.argv[1])
