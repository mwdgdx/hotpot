class Solution {
public:
    int maxTurbulenceSize(vector<int>& A) {
        if(A.size()==0) return 0;
        int cur = 0;
        int maxLength=1;
        for(int i=0, j =1; j<A.size(); j++){
            if(A[j]==A[j-1]){
                i=j;
                cur=0;
            }else
            if(A[j-1]>A[j]){
                if(cur==1){
                    cur=1;
                    i=j-1;
                    continue;
                } else{
                    cur = 1;
                    maxLength=max(j-i+1, maxLength);
                }
            }else{
                if(cur==-1){
                    cur=-1;
                    i=j-1;
                    continue;
                } else{
                    cur=-1;
                    maxLength=max(j-i+1, maxLength);
                }
            }
            
        }
        return maxLength;
    }
};
// 用cur 记录下一个需要的方向
// 遇到相同的两个点 就回归一个的window size
// 方向不一致 就回归到两个的window size
// 方向一致就 继续
