/* Link to the problem: https://leetcode.com/explore/challenge/card/30-day-leetcoding-challenge/528/week-1/3284 */

class Solution {
    int func(int n){
        int sum = 0;
        while(n){
            int digit = n %  10;
            n /= 10;
            sum += digit * digit;
        }
        return sum;
    }
public:
    bool isHappy(int n) {
        std::unordered_set<int> visited;
        while(true){
            n = func(n);
            if(visited.count(n) == 1){
                return false;
            }
            visited.insert(n);
            if(n == 1){
                return true;
            }
            
        }
        
    }
};
