module.exports = 
	{ apps: [ 
		{ nome: 'django-app', 
		  script: 'manage.py', 
                  args: [ 'runserver', '192.168.15.210:5000' ], 
                  intérprete: 'python3', 
                  relógio: true , 
                  ignore_watch: ['node_modules', 'logs'] } ] };
