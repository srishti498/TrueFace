import { useState } from "react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Shield, Brain, Users, MessageSquare, Eye, Target, Zap } from "lucide-react";
import ProfileAnalyzer from "@/components/ProfileAnalyzer";
import truefaceLogo from "@/assets/trueface-logo.png";

const Index = () => {
  const [showAnalyzer, setShowAnalyzer] = useState(false);

  const features = [
    {
      icon: <Brain className="h-6 w-6" />,
      title: "AI-Powered Analysis",
      description: "Advanced algorithms analyze profile patterns and detect anomalies"
    },
    {
      icon: <Users className="h-6 w-6" />,
      title: "Social Metrics",
      description: "Evaluates follower ratios, engagement patterns, and posting behavior"
    },
    {
      icon: <Eye className="h-6 w-6" />,
      title: "Visual Recognition",
      description: "Identifies stock photos, AI-generated images, and suspicious avatars"
    },
    {
      icon: <Target className="h-6 w-6" />,
      title: "Risk Assessment",
      description: "Provides detailed confidence scores and risk factor analysis"
    }
  ];

  const stats = [
    { value: "98.7%", label: "Accuracy Rate" },
    { value: "2.1M+", label: "Profiles Analyzed" },
    { value: "< 2s", label: "Analysis Time" },
    { value: "24/7", label: "Availability" }
  ];

  if (showAnalyzer) {
    return (
      <div className="min-h-screen bg-gradient-background">
        <div className="container mx-auto px-4 py-8">
          {/* Header */}
          <div className="text-center mb-8">
            <div className="flex items-center justify-center gap-3 mb-4">
              <img src={truefaceLogo} alt="Trueface AI" className="h-12 w-12" />
              <h1 className="text-3xl font-bold text-foreground">Trueface AI</h1>
            </div>
            <p className="text-muted-foreground max-w-2xl mx-auto">
              Professional social media profile authenticity analyzer
            </p>
            <button 
              onClick={() => setShowAnalyzer(false)}
              className="text-primary hover:text-primary/80 mt-2 text-sm underline"
            >
              ← Back to overview
            </button>
          </div>

          <ProfileAnalyzer />
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-background">
      <div className="container mx-auto px-4 py-12">
        {/* Hero Section */}
        <div className="text-center mb-16">
          <div className="flex items-center justify-center gap-4 mb-6">
            <img src={truefaceLogo} alt="Trueface AI" className="h-16 w-16 drop-shadow-lg" />
            <div>
              <h1 className="text-5xl font-bold text-foreground mb-2">Trueface AI</h1>
              <Badge className="bg-gradient-cyber text-primary-foreground px-3 py-1">
                Cybersecurity Assistant
              </Badge>
            </div>
          </div>
          
          <p className="text-xl text-muted-foreground max-w-3xl mx-auto mb-8">
            Advanced AI-powered social media profile authenticity analyzer. Detect fake profiles, 
            bots, and suspicious accounts with industry-leading accuracy and comprehensive analysis.
          </p>
          
          <button 
            onClick={() => setShowAnalyzer(true)}
            className="bg-gradient-cyber text-primary-foreground px-8 py-4 rounded-lg font-semibold shadow-cyber hover:shadow-glow transition-all duration-300 text-lg"
          >
            <Shield className="h-5 w-5 mr-2 inline" />
            Start Profile Analysis
          </button>
        </div>

        {/* Stats */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-6 mb-16">
          {stats.map((stat, index) => (
            <Card key={index} className="border-border bg-card/50 shadow-card text-center">
              <CardContent className="pt-6">
                <div className="text-2xl font-bold text-cyber-blue mb-1">{stat.value}</div>
                <div className="text-sm text-muted-foreground">{stat.label}</div>
              </CardContent>
            </Card>
          ))}
        </div>

        {/* Features */}
        <div className="mb-16">
          <h2 className="text-3xl font-bold text-foreground text-center mb-12">
            Advanced Detection Capabilities
          </h2>
          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
            {features.map((feature, index) => (
              <Card key={index} className="border-border bg-card/50 shadow-card hover:shadow-glow transition-all duration-300">
                <CardHeader>
                  <div className="w-12 h-12 bg-gradient-cyber rounded-lg flex items-center justify-center text-primary-foreground mb-4">
                    {feature.icon}
                  </div>
                  <CardTitle className="text-foreground">{feature.title}</CardTitle>
                </CardHeader>
                <CardContent>
                  <CardDescription className="text-muted-foreground">
                    {feature.description}
                  </CardDescription>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>

        {/* How It Works */}
        <Card className="border-border bg-card/50 shadow-card mb-16">
          <CardHeader>
            <CardTitle className="text-foreground text-center text-2xl mb-4">
              How Trueface AI Works
            </CardTitle>
            <CardDescription className="text-muted-foreground text-center max-w-3xl mx-auto">
              Our advanced cybersecurity system analyzes multiple profile indicators to provide 
              accurate authenticity assessments with detailed explanations.
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="grid md:grid-cols-3 gap-8">
              <div className="text-center">
                <div className="w-16 h-16 bg-gradient-cyber rounded-full flex items-center justify-center text-primary-foreground mx-auto mb-4">
                  <MessageSquare className="h-8 w-8" />
                </div>
                <h3 className="text-foreground font-semibold mb-2">1. Data Input</h3>
                <p className="text-muted-foreground text-sm">
                  Enter profile information including username, bio, follower counts, and engagement metrics
                </p>
              </div>
              
              <div className="text-center">
                <div className="w-16 h-16 bg-gradient-cyber rounded-full flex items-center justify-center text-primary-foreground mx-auto mb-4">
                  <Zap className="h-8 w-8" />
                </div>
                <h3 className="text-foreground font-semibold mb-2">2. AI Analysis</h3>
                <p className="text-muted-foreground text-sm">
                  Advanced algorithms process patterns, ratios, and indicators to detect suspicious behavior
                </p>
              </div>
              
              <div className="text-center">
                <div className="w-16 h-16 bg-gradient-cyber rounded-full flex items-center justify-center text-primary-foreground mx-auto mb-4">
                  <Shield className="h-8 w-8" />
                </div>
                <h3 className="text-foreground font-semibold mb-2">3. Detailed Report</h3>
                <p className="text-muted-foreground text-sm">
                  Receive comprehensive results with confidence scores, risk factors, and manual detection tips
                </p>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* CTA */}
        <div className="text-center">
          <h2 className="text-2xl font-bold text-foreground mb-4">
            Ready to Verify Profile Authenticity?
          </h2>
          <p className="text-muted-foreground mb-6 max-w-2xl mx-auto">
            Enter profile data and get instant, professional-grade analysis with detailed insights 
            and actionable recommendations for manual verification.
          </p>
          <button 
            onClick={() => setShowAnalyzer(true)}
            className="bg-gradient-cyber text-primary-foreground px-6 py-3 rounded-lg font-semibold shadow-cyber hover:shadow-glow transition-all duration-300"
          >
            <Eye className="h-4 w-4 mr-2 inline" />
            Begin Analysis
          </button>
        </div>
      </div>
    </div>
  );
};

export default Index;