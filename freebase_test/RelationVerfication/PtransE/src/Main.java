import PCRA_Program.PCRA;
import PTransE.TestRun;
import PTransE.TrainRun;

import java.io.File;
import java.io.IOException;
import java.util.Scanner;

public class Main {

    private static void PCRA_run(int rate) throws IOException {
        /*
        File f = new File("resource/path_data/confident.txt");
        if (!f.exists()) {
            PCRA pcra = new PCRA();
            pcra.run(rate);
        }
        */
        PCRA pcra = new PCRA();
        pcra.run(rate);
    }

    public static void main(String[] args) throws IOException {
        System.out.println("Train or test? y/n");
        Scanner sc = new Scanner(System.in);
        boolean train_flag;
        train_flag = sc.next().equals("y");
        System.out.println("which rate:");
        int rate = sc.nextInt();
        if (rate != 55 && rate != 60 && rate != 65 && rate != 70 && rate != 75 && rate != 80 && rate != 85) {
            System.out.println("error!");
            return;
        }
        if (train_flag) {
            PCRA_run(rate);
            TrainRun trainRun = new TrainRun();
            trainRun.train_run(rate);
        } else {
            TestRun testRun = new TestRun();
            testRun.test_run(rate);
        }
    }
}
