import { Pie1DataProps } from "@/components/Chart";


export const updatePie1Data = (raw: Pie1DataProps['data'], newData: string[]) :Pie1DataProps['data'] => {
    //因为emotion有很多个返回的值，可能存在多个人脸，因此为了通用，需要再度进行遍历
    
    let ret = [...raw];
    
    for(let i = 0; i < newData.length; ++i){
        if(ret.find((x) => x.name === newData[i])){
            ret = ret.map((x) => {
                if(x.name === newData[i]){
                    return {
                    name: x.name,
                    value: x.value + 1, 
                    }
                }
                return x
            })
        }else{
            ret = [...ret, {
                name: newData[i],
                value: 1,
            }]
        }
    }
    
    return ret;
    

}