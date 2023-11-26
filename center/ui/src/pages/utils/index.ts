//计算情感健康度，根据心理分析的权重计算

export const calHealthy = (data: {name: string, value: number}[]) => {

    const projects = Object.create({});
    
    if(!data) return 0;
    
    data.forEach((k) => {
        projects[k.name as string] = k.value
    })
    
    // 每个项目的权重
    const weights = (value: number, min: number, max: number) => {
        const benchMark = ( min + max ) /2
        const s = Math.max(100 - Math.abs(value-benchMark), 0)
        return s/8
    }
    
    const scores = [
        weights(projects['关怀'], -20, 20),
        weights(projects['戒备'], 10, 30),
        weights(projects['同理心'], 0, 40),
        weights(projects['恐慌'], 20, 50),
        weights(projects['自杀倾向'], 0, 50),
        weights(projects['情绪稳定'], 0, 80),
        weights(projects['社交期望'], 20, 40),
        weights(projects['躁动'], 10, 40),
        weights(projects['药物使用'], 20, 60)
    ];

    // 计算总分
    const totalScore = scores.reduce((acc, cur) => acc + cur, 0);

    return Number(totalScore.toFixed(0))
}

export const calHealthyText = (value: number): '优秀' | '良好' | '中等' | '异常'=> {
    if (value >= 87.5) {
      return '优秀';
    } else if (value >= 62.5) {
      return '良好';
    } else if (value >= 37.5) {
      return '中等';
    } else {
      return '异常';
    }
    
}