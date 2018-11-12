package TransH;

import java.io.*;
import java.util.*;

import static TransH.GlobalValue.*;
import static TransH.Gradient.calc_sum;

public class Test {
    // region private members
    private List<Integer> fb_h;
    private List<Integer> fb_t;
    private List<Integer> fb_r;
    private ArrayList<Boolean> label;
    // endregion

    Test() {
        fb_h = new ArrayList<>();
        fb_t = new ArrayList<>();
        fb_r = new ArrayList<>();
        label = new ArrayList<>();
    }

    public void add(int head, int relation, int tail, boolean flag) {
        fb_h.add(head);
        fb_r.add(relation);
        fb_t.add(tail);
        label.add(flag);
    }

    private void Read_Vec_File(String file_name, double[][] vec) throws IOException {
        File f = new File(file_name);
        BufferedReader reader = new BufferedReader(new InputStreamReader(new FileInputStream(f),"UTF-8"));
        String line;
        for (int i = 0; (line = reader.readLine()) != null; i++) {
            String[] line_split = line.split("\t");
            for (int j = 0; j < vector_dimension; j++) {
                vec[i][j] = Double.valueOf(line_split[j]);
            }
        }
    }

    private void relation_add(Map<Integer, Integer> relation_num, int relation) {
        if (!relation_num.containsKey(relation)) {
            relation_num.put(relation, 0);
        }
        int count = relation_num.get(relation);
        relation_num.put(relation, count + 1);
    }

    private void map_add_value(Map<Integer, Integer> tmp_map, int id, int value) {
        if (!tmp_map.containsKey(id)) {
            tmp_map.put(id, 0);
        }
        int tmp_value = tmp_map.get(id);
        tmp_map.put(id, tmp_value + value);
    }

    public void run() throws IOException {
        relation_vec = new double[relation_num][vector_dimension];
        entity_vec = new double[entity_num][vector_dimension];
        Wr_vec = new double[relation_num][vector_dimension];

        Read_Vec_File("resource/result/relation2vec.bern", relation_vec);
        Read_Vec_File("resource/result/entity2vec.bern", entity_vec);
        Read_Vec_File("resource/result/Wr_vec.bern", Wr_vec);

        double TP = 0, FP = 0, TN = 0, FN = 0;

        double margin = 10;
        for (int i = 0; i < fb_h.size(); i++) {

            boolean flag = label.get(i);

            double dis = calc_sum(fb_h.get(i), fb_t.get(i), fb_r.get(i));

            boolean pred;

            if (dis < margin) {
                pred = true;
            }
            else {
                pred = false;
            }

            if (pred == true) {
                if (flag == true) {
                    TP = TP + 1;
                } else {
                    FP = FP + 1;
                }
            }
            else {
                if (flag == true) {
                    FN = FN + 1;
                } else {
                    TN = TN + 1;
                }
            }
        }

        double precision = TP / (TP + FP);
        double recall = TP / (TP + FN);
        double accuracy = (TP + TN) / (TP + FP + TN + FN);
        double F1 = (2.0 * TP) / (2.0 * TP + FP + FN);

        System.out.println("TP: " + TP + " FP: "+ FP + " TN: " + TN + " FN: " + FN);
        System.out.println("precision: " + precision);
        System.out.println("recall: " + recall);
        System.out.println("accuracy: " + accuracy);
        System.out.println("F1: " + F1);

    }

}
