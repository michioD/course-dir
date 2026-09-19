import java.util.*;
// import java.time.LocalDate;
// import java.time.format.DateTimeFormatter;
// local date way too expensive bruh ;-;

class Student implements Comparable<Student>{
    String name;
    String [] names;
    int dateOfSubmission;
    String lastName;
    public Student(String name, int dateOfSubmission){
        this.name = name;
        // date of submission is in YYYYMMDD 
        // to obtain YYYY you just floor divide by 10000
        // to obtain MM you floor divide by 100 and mod by 100
        // to obtain DD you just mod by 100
        this.dateOfSubmission = dateOfSubmission;
        this.names = this.name.split("\\s+");
        this.lastName = this.names[this.names.length-1];
    }
    @Override
    public int compareTo(Student other) {
        if (this.dateOfSubmission != other.dateOfSubmission){
            return Integer.compare(this.dateOfSubmission, other.dateOfSubmission);
        }
        if (!this.lastName.equals(other.lastName)){
            return this.lastName.compareTo(other.lastName);
        }
        if (!this.names[0].equals(other.names[0])){
            return this.names[0].compareTo(other.names[0]);
        }
        // compare middle names
        for (int i = 1; i < Math.min(this.names.length, other.names.length) - 1; i++){
            if (!this.names[i].equals(other.names[i])){
                return this.names[i].compareTo(other.names[i]);
            }
        }
        if(this.names.length != other.names.length){
            return this.names.length - other.names.length;
        }
        return 0;
    }
    @Override
    public String toString(){
        return this.name;
    }
    public void setDateOfSubmission(int dateOfSubmission){
        this.dateOfSubmission = dateOfSubmission;
    }
    public String getName(){
        return this.name;
    }
    public int getDateOfSubmission(){
        return this.dateOfSubmission;
    }
    public String getLastName(){
        return this.lastName;
    }
    private static int getDateOfPresentation(int dateOfSubmission){
        int result = dateOfSubmission;

        // break down the dates using modular operatin?
        
        int day = dateOfSubmission % 100;
        // diviide out the month
        int month = (dateOfSubmission / 100) % 100;
        int year = dateOfSubmission / 10000;

        if (1 <= day && day < 15){
            result = year *10000 +month*100 + 15;
        } else{
            // new years need to reset to january next year
            if (month == 12){
                result = (year + 1) * 10000 + 101;
            } else{
                // goes forward one month resets to 1st
                result = year*10000 +(month+1)*100+01;
            }
        }
        return result;
    }
    private static int getNextPresentationDate(int presentationDate){
        return getDateOfPresentation(presentationDate);
    }

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        ArrayList<Student> students = new ArrayList<>();
        while(scanner.hasNextLine()){
            String temp = scanner.nextLine();
            if (temp.isEmpty()){
                break;
            }
            String[] inputData = temp.trim().split("\\s(?=\\d)", 2); // regex that specifically finds white spaces with a digit look ahead
            int dateOfSubmission = Integer.parseInt(inputData[1]);
            String student = inputData[0];
            students.add(new Student(student, dateOfSubmission));
        }
        // ill assume the students will be printed in the correct order since its iterated after its sorted
        Collections.sort(students);
        HashMap<String, Integer> presentationDateOfEachLastName = new HashMap<>();
        // make treemap for this instead keeps the keys sorted
        TreeMap<Integer, ArrayList<Student>> studentsOfEachPresentationDate = new TreeMap<>();

        for (int i = 0; i < students.size(); i++){
            Student student = students.get(i);
            int presentationDate = getDateOfPresentation(student.getDateOfSubmission());
            // attempts to find if this submission date and last name has been assigned before
            if (i > 0){
                if (presentationDateOfEachLastName.containsKey(student.getDateOfSubmission()+student.getLastName())){
                    presentationDate = presentationDateOfEachLastName.get(student.getDateOfSubmission()+student.getLastName());
                    studentsOfEachPresentationDate.get(presentationDate).add(student);
                    continue;
                }
            }

            // if its a new presentation date then add it 
            if (!studentsOfEachPresentationDate.containsKey(presentationDate)){
                studentsOfEachPresentationDate.put(presentationDate, new ArrayList<>());
                studentsOfEachPresentationDate.get(presentationDate).add(student);
                presentationDateOfEachLastName.put(student.getDateOfSubmission()+student.getLastName(), presentationDate);
                continue;
            }


            // get the tail key of studentsOfEachPresentationDate
            int latestDate = studentsOfEachPresentationDate.lastKey();
            if (studentsOfEachPresentationDate.get(latestDate).size() < 5){
                studentsOfEachPresentationDate.get(latestDate).add(student);
                presentationDateOfEachLastName.put(student.getDateOfSubmission()+student.getLastName(), latestDate);
                continue;
                
            } else{
                // if the presentation date is full then we need to find the next available presentation date
                int nextPresentationDate = getNextPresentationDate(latestDate);
                if (!studentsOfEachPresentationDate.containsKey(nextPresentationDate)){
                    studentsOfEachPresentationDate.put(nextPresentationDate, new ArrayList<>());
                }
                studentsOfEachPresentationDate.get(nextPresentationDate).add(student);
                presentationDateOfEachLastName.put(student.getDateOfSubmission()+student.getLastName(), nextPresentationDate);
                continue;
            }
        }
        ArrayList<Integer> presentationDates = new ArrayList<>(studentsOfEachPresentationDate.keySet());
        Collections.sort(presentationDates);
        for (Integer presentationDate: presentationDates){
            ArrayList<Student> studentsOfThisDate = studentsOfEachPresentationDate.get(presentationDate);
            // Collections.sort(studentsOfThisDate);
            System.out.println(presentationDate);
            for (Student student: studentsOfThisDate){
                System.out.println(student.getName());
            }
        }
    }
}
