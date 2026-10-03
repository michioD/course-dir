import java.util.*;
import java.time.LocalDate;
import java.time.format.DateTimeFormatter;

class students{
    private static final DateTimeFormatter formatter = DateTimeFormatter.ofPattern("yyyyMMdd");
    private static String addMonthDay(String date, int months, int days){
        LocalDate dateParsed = LocalDate.parse(date, formatter);
        return dateParsed.plusMonths(months).plusDays(days).format(formatter);
    }
    private static int getDay(String date){
        return Integer.parseInt(date.substring(6,8));
    }

    private static String dateOfPresentation(String dateOfSubmission){
        int dayOfMonth = getDay(dateOfSubmission);
        LocalDate dateParsed = LocalDate.parse(dateOfSubmission, formatter);
        LocalDate result;
        if (dayOfMonth <= 15){
            result = dateParsed.plusDays(15 - dayOfMonth);
        } else{
            result = dateParsed.plusMonths(1).minusDays(dayOfMonth - 1);
        }
        return result.format(formatter);
    }
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        HashMap<String, ArrayList<String>> map = new HashMap<>();
        while(scanner.hasNextLine()){

            String temp = scanner.nextLine();
            if (temp.isEmpty()){
                break;
            }

            String[] inputData = temp.trim().split("\\s(?=\\d)", 2);
            String dateOfSubmission = inputData[1];
            String val = inputData[0];
            String currentKey = dateOfPresentation(dateOfSubmission);

            if (!map.containsKey(currentKey)){
                map.put(currentKey, new ArrayList<>());
                map.get(currentKey).add(val);
            } else if(5 <= map.get(currentKey).size()){
                while(5 <= map.get(currentKey).size()){
                    if (getDay(dateOfSubmission) == 15){
                        currentKey = addMonthDay(dateOfSubmission, 1, -14);
                    }else if (getDay(dateOfSubmission) == 1){
                        currentKey = addMonthDay(dateOfSubmission, 0, 14);
                    }
                    if (!map.containsKey(currentKey)){
                        map.put(currentKey, new ArrayList<>());
                        map.get(currentKey).add(val);
                        break;
                    } 
                    if (map.containsKey(currentKey) && map.get(currentKey).size()<=5){
                        map.get(currentKey).add(val);
                        break;
                    }
                }
            } else{
                map.get(currentKey).add(val);
            }
        }
            List<String> dates = new ArrayList<>(map.keySet());
            Collections.sort(dates);
            for (String date: dates){
                System.out.println(date);
                Collections.sort(map.get(date));
                for (String student : map.get(date)){
                    System.out.println(student);
                }
 
            }


    }
}
