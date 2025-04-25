from FinalVersion.Analysis.ImageAnalysis import AnalyseImage


def bayesianEvaluation(canny_minimum, canny_maximum, canny_ksize,canny_sigma,gaussian_fidelity,gaussian_range,points,y=150,x=150):
    result=0

    for type, original_image in points:
        final_pores=AnalyseImage(original_image,canny_minimum, canny_maximum, canny_ksize,canny_sigma,gaussian_fidelity,gaussian_range,overlay=False)
        if final_pores[y,x]==200 and type=="background":
            result+=1
        elif final_pores[y,x]==0 and type=="pore":
            result+=1
    return float(result/len(points))