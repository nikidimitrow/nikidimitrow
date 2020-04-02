class Solution {
public:
    int singleNumber(std::vector<int>& nums) {
        
        int x = 0;
       
        for(int a : nums)
        {
            x ^= a;
        }
        return x;
    }
};
