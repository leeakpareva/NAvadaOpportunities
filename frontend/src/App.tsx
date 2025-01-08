import { useState } from 'react';
import { Brain, Search, Filter, Bell } from 'lucide-react';
import { CVUpload } from './components/CVUpload';
import { JobMatches } from './components/JobMatches';
import { NotificationTest } from './components/NotificationTest';
import { updateProfile, getJobMatches } from './lib/api';
import type { CVParseResponse, JobMatch } from './types/files';
import { motion } from 'framer-motion';
import { Input } from './components/ui/input';
import { Button } from './components/ui/button';
import { Tabs, TabsContent, TabsList, TabsTrigger } from './components/ui/tabs';
import { Card, CardHeader, CardTitle, CardDescription } from './components/ui/card';

export default function App() {
  const [searchTerm, setSearchTerm] = useState('');
  
  const [opportunities, setOpportunities] = useState<JobMatch[]>([]);
  // Track application status
  const [applicationStatus, setApplicationStatus] = useState<'idle' | 'uploading' | 'matching'>('idle');

  const handleCVUpload = async (data: CVParseResponse['data']) => {
    try {
      setApplicationStatus('uploading');
      console.log('Processing CV data:', data);
      
      // Create anonymous profile for job matching
      const sessionId = 'session_' + Date.now();
      console.log('Created session ID:', sessionId);
      
      await updateProfile({
        userId: sessionId,
        cvData: data,
        preferences: {
          job_types: ['remote'],
          notifications: {
            email: true,
            daily_summary: true
          }
        }
      });
      
      setApplicationStatus('matching');
      console.log('Profile updated, fetching matches...');
      
      // Fetch matching jobs with broader criteria
      const response = await getJobMatches(sessionId, {
        remoteOnly: true,
        employmentTypes: ['full-time', 'contract', 'self-employed', 'freelance']
      });
      
      console.log('Received matches:', response);
      if (response.matches && response.matches.length > 0) {
        setOpportunities(response.matches);
      } else {
        console.log('No matches found');
      }
    } catch (error) {
      console.error('Error processing CV:', error);
      // Show error in UI
      setOpportunities([]);
    } finally {
      setApplicationStatus('idle');
    }
  };

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
            <motion.div className="space-y-6">
              <motion.div
                whileHover={{ scale: 1.1, rotate: 360 }}
                transition={{ duration: 0.5 }}
              >
                <Brain className="w-24 h-24 text-white mb-4" />
              </motion.div>
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
            <div className="flex gap-2 items-center">
              <motion.div 
                className="relative group flex-1"
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
              <motion.div whileHover={{ scale: 1.05 }}>
                <Button 
                  variant="outline" 
                  size="sm" 
                  className="border-white/20 text-white hover:bg-white/10 transition-colors h-12"
                  onClick={() => {
                    if (searchTerm.trim()) {
                      console.log('Searching for:', searchTerm);
                      // Add search logic here
                    }
                  }}
                >
                  <Search className="h-4 w-4 mr-2" />
                  Search
                </Button>
              </motion.div>
            </div>
            
            <div className="flex flex-col gap-2">
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
              <div className="flex">
                <motion.div whileHover={{ scale: 1.05 }}>
                  <CVUpload 
                    onUploadSuccess={handleCVUpload}
                    onUploadError={(error) => console.error(error)}
                  />
                </motion.div>
              </div>
            </div>
          </motion.div>

          <motion.div 
            className="max-w-4xl mx-auto mt-8"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.4 }}
          >
            <Tabs defaultValue="opportunities" className="w-full">
              <TabsList className="grid w-full grid-cols-4 bg-white/5">
                <TabsTrigger value="opportunities" className="data-[state=active]:bg-white/10">Opportunities</TabsTrigger>
                <TabsTrigger value="applied" className="data-[state=active]:bg-white/10">Applied</TabsTrigger>
                <TabsTrigger value="insights" className="data-[state=active]:bg-white/10">Insights</TabsTrigger>
                <TabsTrigger value="notifications" className="data-[state=active]:bg-white/10">Notifications</TabsTrigger>
              </TabsList>
              
              <TabsContent value="opportunities" className="space-y-4 mt-4">
                <motion.div variants={container} initial="hidden" animate="show">
                  <motion.div variants={item}>
                    <JobMatches 
                      matches={opportunities}
                      isLoading={applicationStatus !== 'idle'}
                    />
                  </motion.div>
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

              <TabsContent value="notifications">
                <Card className="bg-white/5 border-white/10">
                  <CardHeader>
                    <CardTitle className="text-white">Notification Settings</CardTitle>
                    <CardDescription className="text-white/60">Configure and test Slack notifications</CardDescription>
                  </CardHeader>
                  <div className="p-6">
                    <NotificationTest />
                  </div>
                </Card>
              </TabsContent>
            </Tabs>
          </motion.div>
        </motion.div>
      </div>
    </div>
  );
}
