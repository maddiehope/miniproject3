CREATE TABLE product (

/* below are the tags for the columns of this sql table .*/
/* all of the values have the parameter 'NOT NULL' because they are required .*/
/* the html form in which these values are collected is coded in a way to ensure that these values are filled before the form is submitted to prevent errors from occuring .*/
    category TEXT NOT NULL,
    description TEXT NOT NULL,
    price INT NOT NULL,
    /* an error method was created in the program to render a custom error page if the code entered by the user is not unique .*/
    code TEXT UNIQUE
); 