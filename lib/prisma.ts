import { PrismaClient } from '@prisma/client';

const globalForPrisma = global as unknown as { prisma: PrismaClient };

export const prisma = globalForPrisma.prisma || new PrismaClient();

if (process.env.NODE_ENif (process.env.NODE_ENialForif (process.env.NODE_ENif (proce. �if (process.env.NODE_ENif (process.��if (process.en�ة البيانات تلقائياً
cat << 'EOF' > app/api/agent/route.ts
import { NextResponse } from 'next/server';
import { prisma } from '@/lib/prisma';

export async function POST(request: Request) {
  try {
                   =                    =                    =     return NextResponse.json({ error: 'Task description is required' }, {                    =                   se = await fetch('http://localhost:8000/run', {
      method: 'POST',
      header      header      ': 'application/json' },
                                          });

    if (!respons    if (!respons    if (!respons    if (!respons    if (!respons    if (!rpo    if (!re`)    if (!respons    if (!rawa    if (!respons    if (!respons    if (!respeate({
      data: {
        prompt: task,
        status: 'RUNNING',
      },
    });

    return NextResponse.json(data);
  } catch (error: an  } catch (error: an  } catch (error: an  } catch (error: an  } catch (error: an  } catch (error: an  } catch (error: an  } catch (error: an  } catch (error: an  } catch (errconst tasks = await prisma.task.findMany({
      orderBy: { createdAt: 'desc' },
      take: 20,
    });
    return NextResponse.json(tasks);
  } catch (error: any) {
           NextResponse.json({ error: error.message }, { status: 500 });
  }
}
