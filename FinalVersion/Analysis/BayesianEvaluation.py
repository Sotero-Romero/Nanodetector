from FinalVersion.Analysis.ImageAnalysis import AnalyseImage


def bayesianEvaluation(fidelity, mean_weight,mean_range,points,y=150,x=150):
    result=0
    pore_cut_off = 3

    for type, original_image in points:
        final_pores=AnalyseImage(original_image,mean_weight,mean_range,pore_cut_off,fidelity,overlay=False)
        if final_pores[y,x]==200 and type=="background":
            result+=1
        elif final_pores[y,x]==0 and type=="pore":
            result+=1
    return float(result/len(points))