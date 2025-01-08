import { useState } from 'react';
import { Brain, Search, Sparkles, Filter, Bell } from 'lucide-react';
import { motion } from 'framer-motion';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';

export default function App() {
  const [searchTerm, setSearchTerm] = useState('');
  
  const opportunities = [
    {
      id: 1,
      title: "AI Art Director",
      company: "Creative Futures Inc.",
      location: "Remote",
      techScore: 0.9,
      artisticScore: 0.85,
      tags: ["AI", "Creative Direction", "Digital Art"],
      description: "Lead the development of AI-powered creative tools and direct artistic vision.",
    },
    {
      id: 2,
      title: "Blockchain Creative Developer",
      company: "Web3 Studios",
      location: "San Francisco, CA",
      techScore: 0.95,
      artisticScore: 0.8,
      tags: ["Blockchain", "Creative Coding", "NFT"],
      description: "Create innovative blockchain-based artistic experiences and NFT platforms.",
    }
  ];

  const container = {
    hidden: { opacity: 0 },
    show: {
      opacity: 1,
      transition: {
        staggerChildren: 0.1
      }
    }
  };

  const item = {
    hidden: { opacity: 0, y: 20 },
    show: { opacity: 1, y: 0 }
  };

  return (
    <div className="min-h-screen bg-background text-foreground overflow-hidden">
      <div className="relative min-h-screen bg-grid-white/10">
        <div className="absolute inset-0 bg-gradient-to-t from-background to-transparent" />
        
        <motion.div 
          className="relative container mx-auto px-4 py-8"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.6 }}
        >
          <motion.div 
            className="flex flex-col items-center mb-12"
            initial={{ y: -50 }}
            animate={{ y: 0 }}
            transition={{ type: "spring", stiffness: 100 }}
          >
            <motion.div
              whileHover={{ scale: 1.1, rotate: 360 }}
              transition={{ duration: 0.5 }}
            >
              <Brain className="w-24 h-24 text-white mb-4" />
            </motion.div>
            <motion.h1 
              className="text-6xl font-bold text-white"
              initial={{ scale: 0.5 }}
              animate={{ scale: 1 }}
              transition={{ type: "spring", stiffness: 200 }}
            >
              NAVADA
            </motion.h1>
            <motion.p 
              className="text-xl text-white/80 mt-4 text-center max-w-2xl"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.2 }}
            >
              Navigating Advanced Technology and Artistic Vision Job Finder
            </motion.p>
          </motion.div>

          <motion.div 
            className="max-w-4xl mx-auto space-y-4"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3 }}
          >
            <motion.div 
              className="relative group"
              whileHover={{ scale: 1.01 }}
              transition={{ duration: 0.2 }}
            >
              <Search className="absolute left-3 top-3 h-5 w-5 text-white/60" />
              <Input
                type="text"
                placeholder="Search for opportunities..."
                className="pl-10 h-12 bg-white/5 border-white/10 focus:border-white/20 transition-all duration-300 hover:bg-white/10 text-white placeholder:text-white/60"
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
              />
            </motion.div>
            
            <div className="flex gap-2">
              <motion.div whileHover={{ scale: 1.05 }}>
                <Button variant="outline" size="sm" className="border-white/20 text-white hover:bg-white/10 transition-colors">
                  <Filter className="h-4 w-4 mr-2" />
                  Filters
                </Button>
              </motion.div>
              <motion.div whileHover={{ scale: 1.05 }}>
                <Button variant="outline" size="sm" className="border-white/20 text-white hover:bg-white/10 transition-colors">
                  <Bell className="h-4 w-4 mr-2" />
                  Notifications
                </Button>
              </motion.div>
            </div>
          </motion.div>

          <motion.div 
            className="max-w-4xl mx-auto mt-8"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.4 }}
          >
            <Tabs defaultValue="opportunities" className="w-full">
              <TabsList className="grid w-full grid-cols-3 bg-white/5">
                <TabsTrigger value="opportunities" className="data-[state=active]:bg-white/10">Opportunities</TabsTrigger>
                <TabsTrigger value="applied" className="data-[state=active]:bg-white/10">Applied</TabsTrigger>
                <TabsTrigger value="insights" className="data-[state=active]:bg-white/10">Insights</TabsTrigger>
              </TabsList>
              
              <TabsContent value="opportunities" className="space-y-4 mt-4">
                <motion.div variants={container} initial="hidden" animate="show">
                  {opportunities.map((job) => (
                    <motion.div key={job.id} variants={item}>
                      <Card className="bg-white/5 backdrop-blur-sm border-white/10 hover:bg-white/10 transition-all duration-300">
                        <CardHeader>
                          <div className="flex justify-between items-start">
                            <div>
                              <CardTitle className="text-xl mb-1 text-white">{job.title}</CardTitle>
                              <CardDescription className="text-white/60">{job.company} • {job.location}</CardDescription>
                            </div>
                            <motion.div whileHover={{ scale: 1.05 }}>
                              <Button size="sm" className="bg-white/10 hover:bg-white/20 text-white">
                                <Sparkles className="h-4 w-4 mr-2" />
                                Apply Now
                              </Button>
                            </motion.div>
                          </div>
                        </CardHeader>
                        <CardContent>
                          <p className="text-sm text-white/60 mb-3">{job.description}</p>
                          <div className="flex gap-2 flex-wrap">
                            {job.tags.map((tag) => (
                              <Badge key={tag} variant="secondary" className="bg-white/5 text-white hover:bg-white/10 transition-colors">
                                {tag}
                              </Badge>
                            ))}
                          </div>
                          <div className="flex gap-4 mt-4">
                            <div className="flex items-center gap-2">
                              <div className="text-xs text-white/60">Tech Score</div>
                              <Badge variant="outline" className="bg-white/5 border-white/20 text-white">
                                {(job.techScore * 100).toFixed(0)}%
                              </Badge>
                            </div>
                            <div className="flex items-center gap-2">
                              <div className="text-xs text-white/60">Artistic Score</div>
                              <Badge variant="outline" className="bg-white/5 border-white/20 text-white">
                                {(job.artisticScore * 100).toFixed(0)}%
                              </Badge>
                            </div>
                          </div>
                        </CardContent>
                      </Card>
                    </motion.div>
                  ))}
                </motion.div>
              </TabsContent>
              
              <TabsContent value="applied">
                <Card className="bg-white/5 border-white/10">
                  <CardHeader>
                    <CardTitle className="text-white">Applied Opportunities</CardTitle>
                    <CardDescription className="text-white/60">Track your applications and their status</CardDescription>
                  </CardHeader>
                </Card>
              </TabsContent>
              
              <TabsContent value="insights">
                <Card className="bg-white/5 border-white/10">
                  <CardHeader>
                    <CardTitle className="text-white">Analytics & Insights</CardTitle>
                    <CardDescription className="text-white/60">View trends and performance metrics</CardDescription>
                  </CardHeader>
                </Card>
              </TabsContent>
            </Tabs>
          </motion.div>
        </motion.div>
      </div>
    </div>
  );
}