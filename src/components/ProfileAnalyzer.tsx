import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { Progress } from "@/components/ui/progress";
import { Badge } from "@/components/ui/badge";
import { Shield, AlertTriangle, CheckCircle, Users, Calendar, Image, MessageSquare, TrendingUp, Eye } from "lucide-react";

interface ProfileData {
  username: string;
  profilePhoto: string;
  bio: string;
  followers: string;
  following: string;
  posts: string;
  engagement: string;
  accountAge: string;
}

interface AnalysisResult {
  verdict: "Real" | "Fake";
  confidence: number;
  explanation: string;
  riskFactors: string[];
  tips: string[];
}

const ProfileAnalyzer = () => {
  const [profileData, setProfileData] = useState<ProfileData>({
    username: "",
    profilePhoto: "",
    bio: "",
    followers: "",
    following: "",
    posts: "",
    engagement: "",
    accountAge: ""
  });

  const [analysisResult, setAnalysisResult] = useState<AnalysisResult | null>(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);

  const analyzeProfile = () => {
    setIsAnalyzing(true);
    
    // Simulate analysis delay
    setTimeout(() => {
      const analysis = performAnalysis(profileData);
      setAnalysisResult(analysis);
      setIsAnalyzing(false);
    }, 2000);
  };

  const performAnalysis = (data: ProfileData): AnalysisResult => {
    let suspicionScore = 0;
    const riskFactors: string[] = [];
    
    // Username analysis
    if (data.username.includes("_") && /\d{4,}/.test(data.username)) {
      suspicionScore += 20;
      riskFactors.push("Username contains multiple underscores and numbers");
    }
    
    // Profile photo analysis
    if (data.profilePhoto.toLowerCase().includes("no") || data.profilePhoto.toLowerCase().includes("none")) {
      suspicionScore += 25;
      riskFactors.push("No profile photo");
    } else if (data.profilePhoto.toLowerCase().includes("stock") || data.profilePhoto.toLowerCase().includes("generic")) {
      suspicionScore += 30;
      riskFactors.push("Generic or stock photo detected");
    }
    
    // Follower ratio analysis
    const followers = parseInt(data.followers) || 0;
    const following = parseInt(data.following) || 0;
    if (following > 0 && followers / following < 0.1) {
      suspicionScore += 25;
      riskFactors.push("Very low follower-to-following ratio");
    }
    if (following > 2000 && followers < 100) {
      suspicionScore += 35;
      riskFactors.push("Following many accounts but very few followers");
    }
    
    // Bio analysis
    if (!data.bio || data.bio.length < 10) {
      suspicionScore += 15;
      riskFactors.push("No bio or very short bio");
    } else if (data.bio.includes("🔥") || data.bio.includes("💯") || data.bio.includes("👑")) {
      suspicionScore += 10;
      riskFactors.push("Bio contains common spam emojis");
    }
    
    // Posts analysis
    const posts = parseInt(data.posts) || 0;
    if (posts < 5) {
      suspicionScore += 20;
      riskFactors.push("Very few posts");
    }
    
    // Engagement analysis
    if (data.engagement.toLowerCase().includes("low") || data.engagement.toLowerCase().includes("poor")) {
      suspicionScore += 15;
      riskFactors.push("Low engagement rates");
    }
    
    // Account age analysis
    if (data.accountAge.toLowerCase().includes("new") || data.accountAge.toLowerCase().includes("recent")) {
      suspicionScore += 20;
      riskFactors.push("Recently created account");
    }
    
    const confidence = Math.min(95, Math.max(5, suspicionScore > 50 ? suspicionScore : 100 - suspicionScore));
    const verdict = suspicionScore > 50 ? "Fake" : "Real";
    
    const explanation = suspicionScore > 50
      ? `High suspicion indicators detected. ${riskFactors.length} red flags identified.`
      : riskFactors.length > 0
      ? `Some minor concerns but profile appears legitimate. ${riskFactors.length} potential issues noted.`
      : "Profile shows strong indicators of authenticity with no major red flags.";
    
    const tips = [
      "Check for consistent posting patterns over time",
      "Verify if the profile photo appears in reverse image searches",
      "Look for genuine interactions in comments and replies",
      "Cross-reference information with other social platforms",
      "Be wary of profiles with very new creation dates",
      "Check if follower growth seems organic or suspicious"
    ];
    
    return { verdict, confidence, explanation, riskFactors, tips };
  };

  const handleInputChange = (field: keyof ProfileData, value: string) => {
    setProfileData(prev => ({ ...prev, [field]: value }));
  };

  const resetAnalysis = () => {
    setAnalysisResult(null);
    setProfileData({
      username: "",
      profilePhoto: "",
      bio: "",
      followers: "",
      following: "",
      posts: "",
      engagement: "",
      accountAge: ""
    });
  };

  return (
    <div className="space-y-6">
      {/* Input Form */}
      <Card className="border-border bg-card shadow-card">
        <CardHeader>
          <CardTitle className="text-foreground flex items-center gap-2">
            <Eye className="h-5 w-5 text-primary" />
            Profile Data Input
          </CardTitle>
          <CardDescription className="text-muted-foreground">
            Enter the social media profile information for analysis. Fill out as many fields as possible for accurate results.
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="space-y-2">
              <Label htmlFor="username" className="text-foreground">Username</Label>
              <Input
                id="username"
                placeholder="@username or handle"
                value={profileData.username}
                onChange={(e) => handleInputChange("username", e.target.value)}
                className="bg-input border-border"
              />
            </div>
            
            <div className="space-y-2">
              <Label htmlFor="profilePhoto" className="text-foreground">Profile Photo Info</Label>
              <Input
                id="profilePhoto"
                placeholder="e.g., 'No photo', 'Stock image', 'Personal photo'"
                value={profileData.profilePhoto}
                onChange={(e) => handleInputChange("profilePhoto", e.target.value)}
                className="bg-input border-border"
              />
            </div>
            
            <div className="space-y-2">
              <Label htmlFor="followers" className="text-foreground">Followers Count</Label>
              <Input
                id="followers"
                type="number"
                placeholder="Number of followers"
                value={profileData.followers}
                onChange={(e) => handleInputChange("followers", e.target.value)}
                className="bg-input border-border"
              />
            </div>
            
            <div className="space-y-2">
              <Label htmlFor="following" className="text-foreground">Following Count</Label>
              <Input
                id="following"
                type="number"
                placeholder="Number of accounts following"
                value={profileData.following}
                onChange={(e) => handleInputChange("following", e.target.value)}
                className="bg-input border-border"
              />
            </div>
            
            <div className="space-y-2">
              <Label htmlFor="posts" className="text-foreground">Posts Count</Label>
              <Input
                id="posts"
                type="number"
                placeholder="Total number of posts"
                value={profileData.posts}
                onChange={(e) => handleInputChange("posts", e.target.value)}
                className="bg-input border-border"
              />
            </div>
            
            <div className="space-y-2">
              <Label htmlFor="engagement" className="text-foreground">Engagement Pattern</Label>
              <Input
                id="engagement"
                placeholder="e.g., 'High', 'Low', 'Average'"
                value={profileData.engagement}
                onChange={(e) => handleInputChange("engagement", e.target.value)}
                className="bg-input border-border"
              />
            </div>
            
            <div className="space-y-2">
              <Label htmlFor="accountAge" className="text-foreground">Account Age</Label>
              <Input
                id="accountAge"
                placeholder="e.g., '2 years', 'New account', '6 months'"
                value={profileData.accountAge}
                onChange={(e) => handleInputChange("accountAge", e.target.value)}
                className="bg-input border-border"
              />
            </div>
          </div>
          
          <div className="space-y-2">
            <Label htmlFor="bio" className="text-foreground">Bio/Description</Label>
            <Textarea
              id="bio"
              placeholder="Enter the profile bio or description text..."
              value={profileData.bio}
              onChange={(e) => handleInputChange("bio", e.target.value)}
              className="bg-input border-border min-h-[100px]"
            />
          </div>
          
          <div className="flex gap-3">
            <Button 
              onClick={analyzeProfile} 
              disabled={isAnalyzing}
              className="bg-gradient-cyber text-primary-foreground shadow-cyber hover:shadow-glow transition-all duration-300"
            >
              {isAnalyzing ? (
                <>
                  <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-primary-foreground mr-2" />
                  Analyzing...
                </>
              ) : (
                <>
                  <Shield className="h-4 w-4 mr-2" />
                  Analyze Profile
                </>
              )}
            </Button>
            
            <Button 
              variant="outline" 
              onClick={resetAnalysis}
              className="border-border text-foreground hover:bg-muted"
            >
              Reset
            </Button>
          </div>
        </CardContent>
      </Card>

      {/* Analysis Results */}
      {analysisResult && (
        <Card className="border-border bg-card shadow-card">
          <CardHeader>
            <CardTitle className="text-foreground flex items-center gap-2">
              {analysisResult.verdict === "Real" ? (
                <CheckCircle className="h-5 w-5 text-cyber-green" />
              ) : (
                <AlertTriangle className="h-5 w-5 text-cyber-red" />
              )}
              Analysis Results
            </CardTitle>
            <CardDescription className="text-muted-foreground">
              Comprehensive authenticity assessment based on provided data
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-6">
            {/* Verdict and Confidence */}
            <div className="flex items-center justify-between p-4 rounded-lg border border-border bg-muted/20">
              <div className="space-y-1">
                <div className="flex items-center gap-2">
                  <Badge 
                    variant={analysisResult.verdict === "Real" ? "default" : "destructive"}
                    className={analysisResult.verdict === "Real" 
                      ? "bg-gradient-success text-accent-foreground" 
                      : "bg-gradient-danger text-destructive-foreground"
                    }
                  >
                    {analysisResult.verdict} Profile
                  </Badge>
                  <span className="text-lg font-semibold text-foreground">
                    {analysisResult.confidence}% Confidence
                  </span>
                </div>
                <p className="text-muted-foreground text-sm">{analysisResult.explanation}</p>
              </div>
              <div className="text-right">
                <div className="w-24 space-y-2">
                  <Progress 
                    value={analysisResult.confidence} 
                    className={`h-2 ${analysisResult.verdict === "Real" ? "text-cyber-green" : "text-cyber-red"}`}
                  />
                  <span className="text-xs text-muted-foreground">Confidence Level</span>
                </div>
              </div>
            </div>

            {/* Risk Factors */}
            {analysisResult.riskFactors.length > 0 && (
              <div className="space-y-3">
                <h3 className="text-foreground font-semibold flex items-center gap-2">
                  <AlertTriangle className="h-4 w-4 text-cyber-orange" />
                  Risk Factors Detected ({analysisResult.riskFactors.length})
                </h3>
                <div className="space-y-2">
                  {analysisResult.riskFactors.map((factor, index) => (
                    <div key={index} className="flex items-start gap-2 p-2 rounded border border-destructive/20 bg-destructive/5">
                      <div className="w-2 h-2 bg-cyber-red rounded-full mt-2 flex-shrink-0" />
                      <span className="text-sm text-foreground">{factor}</span>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Manual Detection Tips */}
            <div className="space-y-3">
              <h3 className="text-foreground font-semibold flex items-center gap-2">
                <TrendingUp className="h-4 w-4 text-cyber-blue" />
                Manual Detection Tips
              </h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
                {analysisResult.tips.map((tip, index) => (
                  <div key={index} className="flex items-start gap-2 p-2 rounded border border-primary/20 bg-primary/5">
                    <div className="w-2 h-2 bg-cyber-blue rounded-full mt-2 flex-shrink-0" />
                    <span className="text-sm text-foreground">{tip}</span>
                  </div>
                ))}
              </div>
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
};

export default ProfileAnalyzer;