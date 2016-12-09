import sys

if __name__ == "__main__":
    
    if len(sys.argv) != 3:
        print "Usage: python eval.py <your_predict_file> <origin_data_file>"
        exit(0)
    
    answer_file = sys.argv[1]
    gold_file = sys.argv[2]
    dic = {}

    fin = open(gold_file)
    for line in fin:
        line = line.strip()
        if not line:
            continue
        cols = line.split('\t')
        if cols[0] == 'QuestionID':
            continue

        q_id = cols[0]
        a_id = cols[4]
        
        if not q_id in dic:
            dic[q_id] = {}
        dic[q_id][a_id] = [cols[6],-1]
    fin.close()

    fin = open(answer_file)
    for line in fin:
        line = line.strip()
        if not line:
            continue
        cols = line.split('\t')
        q_id = cols[0]
        a_id = cols[1]
        rank = int(cols[2])
        dic[q_id][a_id][1] = rank
    fin.close()

    MAP = 0.0
    MRR = 0.0
    for q_id in dic:
        sort_rank = sorted(dic[q_id].iteritems(), key = lambda asd:asd[1][1], reverse = False)
        correct = 0
        total = 0
        AP = 0.0
        mrr_mark = False
        for i in range(len(sort_rank)):
            #compute MRR
            if sort_rank[i][1][0] == '1' and mrr_mark == False:
                MRR += 1.0 / float(i + 1)
                mrr_mark = True

            #compute MAP
            total += 1
            if sort_rank[i][1][0] == '1':
                correct += 1
                AP += float(correct) / float(total)
        AP /= float(correct)
        MAP += AP

    MAP /= float(len(dic))
    MRR /= float(len(dic))
    print "Final Evaluation Score:"
    print "MAP:", MAP
    print "MRR", MRR

    exit(0)
    
